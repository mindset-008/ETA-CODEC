from ..wrapper.eta_codec import * # change based on your directory

if __name__ == "__main__":
    test_time = "2025-09-08 14:32:00"
    print("Encoding:", test_time)

    write_eta_file("example.eta", test_time)

    decoded_time = read_eta_file("example.eta")
    print("Decoded:", decoded_time)
