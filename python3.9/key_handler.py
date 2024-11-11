# key_handler.py
import cv2

def handle_key_input(key, effect_type, bRec, outputVideo, output_frame):
    effect_name = {
        0: "Normal",
        1: "Cartoonify",
        2: "Pencil_Sketch",
        3: "Vintage",
        4: "Soft_Focus",
        5: "Virtual Makeup",
        6: "Caricature"
    }

    # 효과 선택 처리
    if ord('0') <= key <= ord('6'):
        effect_type = key - ord('0')
    
    # 스크린샷 저장
    elif key == ord('s'):
        filename = f"{effect_name.get(effect_type, 'Unknown')}_capture.jpg"
        cv2.imwrite(filename, output_frame)
        print(f"이미지 캡처 완료: {filename}")

    # 녹화 시작/중지
    elif key == ord('r'):
        if not bRec:
            outputVideo = cv2.VideoWriter('Video.avi', cv2.VideoWriter_fourcc(*'DIVX'), 30.0, (1280, 720))
            bRec = True
            print("녹화 시작")
        else:
            outputVideo.release()
            bRec = False
            print("녹화 중지")
    
    # 종료
    elif key == ord('q'):
        return None, effect_type, bRec, outputVideo  # 종료 신호
    
    return effect_type, bRec, outputVideo  # 업데이트된 값 반환