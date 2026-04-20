import sys
from docling.document_converter import DocumentConverter

def main():
    file_path = "input/MLOPS/3747346.pdf"
    print(f"Attempting to convert {file_path} using Docling...")
    try:
        converter = DocumentConverter()
        result = converter.convert(file_path)
        doc = result.document.export_to_markdown()
        print("Success!")
        print(doc[:100])
    except Exception as e:
        print(f"Caught expected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
