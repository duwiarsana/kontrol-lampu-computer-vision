import mediapipe
print("Top level dir:", dir(mediapipe))
try:
    import mediapipe.python.solutions as solutions
    print("Imported mediapipe.python.solutions")
    print(dir(solutions))
except ImportError as e:
    print(f"Failed to import mediapipe.python.solutions: {e}")

try:
    from mediapipe import solutions
    print("from mediapipe import solutions success")
except ImportError as e:
    print(f"Failed to from mediapipe import solutions: {e}")
