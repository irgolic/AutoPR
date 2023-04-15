import argparse
import re
import sys

def main():
    parser = argparse.ArgumentParser(description='Automatically append the "Closes #{num}" footer to pull request bodies.')
    parser.add_argument('issue_number', type=int, help='The issue number to reference in the "Closes #" footer.')
    parser.add_argument('input_file', type=argparse.FileType('r'), nargs='?', default=sys.stdin, help='The input file containing the PR body. If not provided, the script will read from stdin.')

    args = parser.parse_args()

    pr_body = args.input_file.read()
    args.input_file.close()

    # Check if a "Closes #" footer already exists
    if re.search(r'Closes\s*#\d+', pr_body, flags=re.IGNORECASE):
        print("A 'Closes #' footer already exists:")
        print(pr_body)
        sys.exit(1)

    # Append the "Closes #{num}" footer to the end of the PR body
    updated_pr_body = f"{pr_body.rstrip()}\n\nCloses #{args.issue_number}"
    print(updated_pr_body)

if __name__ == '__main__':
    main()