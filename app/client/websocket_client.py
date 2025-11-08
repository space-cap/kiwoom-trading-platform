"""
Kiwoom WebSocket Client for Real-time Data
"""

import asyncio
import json
from typing import Optional, Dict, Any, Callable
from datetime import datetime

import websockets
from websockets.client import WebSocketClientProtocol

from app.core.config import get_settings
from app.core.logging import logger
from app.core.security import token_manager
from app.shared.exceptions import AuthenticationException, APIException

settings = get_settings()


class KiwoomWebSocketClient:
    """키움증권 WebSocket 클라이언트"""
    
    def __init__(self):
        # WebSocket URL: wss://api.kiwoom.com:10000/api/dostk/websocket
        base_url = settings.KIWOOM_BASE_URL.replace("https://", "wss://")
        self.uri = f"{base_url}:10000/api/dostk/websocket"
        
        self.websocket: Optional[WebSocketClientProtocol] = None
        self.connected = False
        self.keep_running = True
        self._message_handlers: Dict[str, Callable] = {}
        
    async def connect(self) -> bool:
        """
        WebSocket 서버에 연결
        
        Returns:
            연결 성공 여부
        """
        try:
            logger.info(f"Connecting to WebSocket server: {self.uri}")
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            logger.info("WebSocket connected successfully")
            
            # 로그인 패킷 전송
            access_token = token_manager.get_token()
            if not access_token:
                raise AuthenticationException("No valid access token for WebSocket login")
            
            login_packet = {
                "trnm": "LOGIN",
                "token": access_token
            }
            
            logger.info("Sending LOGIN packet to WebSocket server")
            await self.send_message(login_packet)
            
            return True
            
        except Exception as e:
            logger.error(f"WebSocket connection error: {e}")
            self.connected = False
            return False
    
    async def send_message(self, message: Dict[str, Any]) -> None:
        """
        서버에 메시지 전송
        
        Args:
            message: 전송할 메시지 (dict)
        """
        if not self.connected:
            await self.connect()
        
        if self.connected and self.websocket:
            message_str = json.dumps(message, ensure_ascii=False)
            await self.websocket.send(message_str)
            logger.debug(f"WebSocket message sent: {message.get('trnm')}")
    
    async def receive_messages(self) -> None:
        """서버로부터 메시지 수신 (메인 루프)"""
        while self.keep_running and self.websocket:
            try:
                # 메시지 수신
                response_str = await self.websocket.recv()
                response = json.loads(response_str)
                
                trnm = response.get("trnm")
                
                # LOGIN 응답 처리
                if trnm == "LOGIN":
                    return_code = response.get("return_code")
                    if return_code != 0:
                        error_msg = response.get("return_msg", "Unknown error")
                        logger.error(f"WebSocket login failed: {error_msg}")
                        await self.disconnect()
                    else:
                        logger.info("WebSocket login successful")
                
                # PING 응답 처리 (에코백)
                elif trnm == "PING":
                    await self.send_message(response)
                    logger.debug("PING-PONG")
                
                # 일반 메시지 처리
                else:
                    logger.info(f"WebSocket response received: {trnm}")
                    logger.debug(f"Response data: {response}")
                    
                    # 등록된 핸들러 호출
                    if trnm in self._message_handlers:
                        handler = self._message_handlers[trnm]
                        await handler(response)
                
            except websockets.ConnectionClosed:
                logger.warning("WebSocket connection closed by server")
                self.connected = False
                break
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse WebSocket message: {e}")
            except Exception as e:
                logger.error(f"Error in WebSocket receive loop: {e}")
    
    async def disconnect(self) -> None:
        """WebSocket 연결 종료"""
        self.keep_running = False
        if self.connected and self.websocket:
            await self.websocket.close()
            self.connected = False
            logger.info("WebSocket disconnected")
    
    def register_handler(self, trnm: str, handler: Callable) -> None:
        """
        메시지 타입별 핸들러 등록
        
        Args:
            trnm: 트랜잭션 이름 (예: 'CNSRLST')
            handler: 핸들러 함수 (async function)
        """
        self._message_handlers[trnm] = handler
        logger.debug(f"Handler registered for {trnm}")
    
    async def get_condition_list(self) -> Dict[str, Any]:
        """
        조건검색 목록 조회
        
        Returns:
            조건검색 목록 응답
            {
                'trnm': 'CNSRLST',
                'return_code': 0,
                'return_msg': '',
                'data': [['0', '조건1'], ['1', '조건2'], ...]
            }
        """
        # 응답을 저장할 변수
        response_data = {}
        response_event = asyncio.Event()
        
        # 응답 핸들러
        async def handle_response(response: Dict[str, Any]):
            nonlocal response_data
            response_data = response
            response_event.set()
        
        # 핸들러 등록
        self.register_handler("CNSRLST", handle_response)
        
        # 연결 확인
        if not self.connected:
            await self.connect()
        
        # 조건검색 목록 요청
        request = {"trnm": "CNSRLST"}
        await self.send_message(request)
        logger.info("Condition list request sent")
        
        # 응답 대기 (타임아웃 10초)
        try:
            await asyncio.wait_for(response_event.wait(), timeout=10.0)
        except asyncio.TimeoutError:
            logger.error("Timeout waiting for condition list response")
            raise APIException("Condition list request timeout")
        
        # 응답 검증
        return_code = response_data.get("return_code")
        if return_code != 0:
            error_msg = response_data.get("return_msg", "Unknown error")
            raise APIException(f"Condition list request failed: {error_msg}")
        
        return response_data
    
    async def run(self) -> None:
        """WebSocket 클라이언트 실행 (백그라운드)"""
        await self.connect()
        await self.receive_messages()


# 싱글톤 인스턴스 (필요 시 사용)
_ws_client_instance: Optional[KiwoomWebSocketClient] = None


def get_websocket_client() -> KiwoomWebSocketClient:
    """WebSocket 클라이언트 싱글톤 인스턴스 반환"""
    global _ws_client_instance
    if _ws_client_instance is None:
        _ws_client_instance = KiwoomWebSocketClient()
    return _ws_client_instance
