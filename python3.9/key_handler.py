import cv2

# 효과 이름 상수 정의
def handle_key_input(key, effect_type, bRec, outputVideo, output_frame):
    effect_name = {
        EFFECT_NORMAL: "Normal",
        EFFECT_CARTOONIFY: "Cartoonify",
        EFFECT_PENCIL_SKETCH: "Pencil_Sketch",
        EFFECT_VINTAGE: "Vintage"
    }

    # 효과 선택 처리
    if ord('0') <= key <= ord('3'):
        effect_type = key - ord('0')

    # 스크린샷 저장
    elif key == ord('s'):
        filename = f"{effect_name.get(effect_type, 'Unknown')}_capture.jpg"
        cv2.imwrite(filename, output_frame)
        print(f"이미지 캡처 완료: {filename}")

    # 녹화 시작/중지
    elif key == ord('r'):
        if not bRec:
            # 녹화 시작
            outputVideo = cv2.VideoWriter('Video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30.0, (1280, 720))
            bRec = True
            print("녹화 시작")
        else:
            # 녹화 중지
            outputVideo.release()
            outputVideo = None  # 녹화 종료 후 VideoWriter를 None으로 설정
            bRec = False
            print("녹화 중지")
    
    # 종료
    elif key == ord('q'):
        return None, effect_type, bRec, outputVideo  # 종료 신호
    
    return effect_type, bRec, outputVideo  # 업데이트된 값 반환