import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script analyzing caller-callee relationship between program runs.')
    parser.add_argument('--input', '-i', type=str, required=True, help='path to input (.json) file to process with caller-callee data.')
     
    