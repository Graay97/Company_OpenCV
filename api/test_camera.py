import cv2
import platform

def test_camera():
    """카메라 테스트 함수"""
    try:
        # Windows에서 여러 백엔드 테스트
        if platform.system() == 'Windows':
            backends = [
                (cv2.CAP_DSHOW, "DirectShow"),
                (cv2.CAP_ANY, "Default"),
                (cv2.CAP_MSMF, "Media Foundation")
            ]
            
            for backend, name in backends:
                print(f"\nTrying {name} backend...")
                cap = cv2.VideoCapture(0, backend)
                
                if cap.isOpened():
                    print(f"Success with {name} backend!")
                    ret, frame = cap.read()
                    if ret:
                        print("Successfully read a frame")
                        cv2.imshow('Test Frame', frame)
                        cv2.waitKey(1000)
                    cap.release()
                else:
                    print(f"Failed to open camera with {name} backend")
        else:
            print("\nTrying default backend...")
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print("Success with default backend!")
                ret, frame = cap.read()
                if ret:
                    print("Successfully read a frame")
                    cv2.imshow('Test Frame', frame)
                    cv2.waitKey(1000)
                cap.release()
            else:
                print("Failed to open camera")
                
    except Exception as e:
        print(f"Error during camera test: {str(e)}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()