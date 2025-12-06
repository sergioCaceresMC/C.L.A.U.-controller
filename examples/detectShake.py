from ClauLib.clau import ClauBNO055

def main():
    clau = ClauBNO055("COM5")
    clau.set_shake_umbral(22)
    if clau.calibrate()["status"] == 500: return

    while True:
        data = clau.collect_data()
        if not data:
            continue
        shake = clau.get_shake()
        if shake["shakeStatus"]: print(shake["shakeMagnitude"])


if __name__ == "__main__":
    main()