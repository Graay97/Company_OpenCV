import sys
import os
import platform

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python3.9'))

from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import cv2
import numpy as np
from typing import Optional
import uvicorn
from io import BytesIO
import base64

# 기존 필터 및 설정 import
from filters import filters
from filters.cartoonify import cartoonify_filter
from filters.vintage import vintage_filter
from filters.beauty import beauty_filter
from filters.headband import headband_filter
from utils import initialize_face_detectors
from config import (
    EFFECT_NORMAL, EFFECT_HEADBAND, EFFECT_CARTOONIFY,
    EFFECT_VINTAGE, EFFECT_BEAUTY
)

app = FastAPI(
    title="Filter API",
    description="실시간 필터 적용 API",
    version="1.0.0"
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# 전역 변수
cap = None
detector = None
predictor = None

def apply_filters(frame, effect_type):
    """필터 적용 함수"""
    try:
        if effect_type == EFFECT_NORMAL:
            return frame
        elif effect_type == EFFECT_CARTOONIFY:
            # 직접 cartoonify_filter 함수 import
            from filters.cartoonify import cartoonify_filter
            return cartoonify_filter(frame)
        elif effect_type == EFFECT_VINTAGE:
            # 직접 vintage_filter 함수 import
            from filters.vintage import vintage_filter
            return vintage_filter(frame)
        elif effect_type == EFFECT_HEADBAND:
            # 그레이스케일 변환
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # 얼굴 검출
            faces = detector(gray)
            
            # 검출된 얼굴이 있으면 머리띠 필터 적용
            if len(faces) > 0:
                for face in faces:
                    frame = headband_filter(
                        frame=frame,
                        predictor=predictor,
                        rect=face,
                        gray=gray
                    )
            return frame
        elif effect_type == EFFECT_BEAUTY:
            from filters.beauty import beauty_filter
            return beauty_filter(frame)
        return frame
    except Exception as e:
        print(f"Filter application error: {str(e)}")
        return frame

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {"status": "running", "message": "Filter API is active"}

@app.get("/frame/{effect_type}")
async def get_frame(effect_type: int):
    """프레임 처리 엔드포인트"""
    try:
        global cap
        if cap is None or not cap.isOpened():
            return JSONResponse(
                status_code=500,
                content={"error": "Camera not initialized"}
            )

        ret, frame = cap.read()
        if not ret:
            return JSONResponse(
                status_code=500,
                content={"error": "Failed to read frame"}
            )

        # 프레임 좌우 반전
        frame = cv2.flip(frame, 1)
        
        # 필터 적용
        filtered_frame = apply_filters(frame, effect_type)
        
        # JPEG 품질 설정 (0-100)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
        
        # 이미지 인코딩
        _, buffer = cv2.imencode('.jpg', filtered_frame, encode_param)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return JSONResponse(
            content={"image": img_base64},
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        )

    except Exception as e:
        print(f"Error in get_frame: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/status")
async def get_status():
    """카메라 상태 확인 엔드포인트"""
    global cap
    return {
        "camera_initialized": cap is not None and cap.isOpened(),
        "face_detection_enabled": detector is not None and predictor is not None
    }

def initialize_camera():
    """카메라 초기 함수"""
    try:
        # DirectShow 백엔드로 시도
        print("Initializing camera with DirectShow...")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print("DirectShow failed, trying default backend...")
            cap = cv2.VideoCapture(0)
            
        if not cap.isOpened():
            raise Exception("No camera device found")
            
        # 카메라 설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # 테스트 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            raise Exception("Failed to read test frame")
            
        print("Camera initialized successfully")
        return cap
        
    except Exception as e:
        print(f"Camera initialization error: {str(e)}")
        return None

@app.on_event("startup")
async def startup_event():
    """서버 시작 시 실행되는 이벤트"""
    global cap, detector, predictor
    try:
        print("Initializing face detectors...")
        detector, predictor = initialize_face_detectors()
        
        print("Initializing camera...")
        cap = initialize_camera()
        if cap is None:
            raise Exception("Failed to initialize camera")
            
    except Exception as e:
        print(f"Startup error: {str(e)}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    """서버 종료 시 실행되는 이벤트"""
    global cap
    if cap:
        cap.release()
        print("Camera released")

app.mount("/static", StaticFiles(directory="."), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)