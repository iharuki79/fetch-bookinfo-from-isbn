import sys
from PIL import Image
from pyzbar.pyzbar import decode, ZBarSymbol
import requests
import xml.etree.ElementTree as ET

# NDLサーチのXML用名前空間の定義
ns = {
    "srw": "http://www.loc.gov/zing/srw/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "dcndl": "http://ndl.go.jp/dcndl/terms/",
}


def read_ISBN_from_image(img_path):
    try:
        img = Image.open(img_path)
    except FileNotFoundError:
        print("File not found")
        return None
    except Exception as e:
        print(e)
        return None
    codes = decode(img, symbols=[ZBarSymbol.EAN13])
    book_name_list = []
    for code in codes:
        book_name = read_ISBN(code)
        if book_name is not None:
            book_name_list.append(book_name)
    return book_name_list


def read_ISBN(decoded_data):
    if decoded_data.type != "EAN13" and decoded_data.type != "EAN10":
        return None
    if decoded_data.data.decode("utf-8")[:2] != "97":
        return None
    isbn_code = decoded_data.data.decode("utf-8")
    book_info = fetch_info_from_ndl(isbn_code)
    return get_book_info(book_info)


# 国立国会図書館のAPIを使って書籍情報を取得する
def fetch_info_from_ndl(isbn_code, output_file=None):
    assert len(isbn_code) == 13 or len(isbn_code) == 10
    url = (
        "https://iss.ndl.go.jp/api/sru?"
        + "operation=searchRetrieve"
        + "&version=1.2"
        + "&recordSchema=dcndl"
        + "&onlyBib=true"
        + "&recordPacking=xml"
        + '&query=isbn="'
        + isbn_code
        + '" AND dpid=iss-ndl-opac'
    )
    response = requests.get(url)
    if output_file is not None:
        with open(f"{output_file}.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
    return response.text


def get_book_info(book_info):
    if book_info is None:
        return None
    root = ET.fromstring(book_info)

    # タイトルを取得
    title = root.find(".//dc:title/rdf:Description/rdf:value", ns)
    if title is not None:
        print(f"タイトル: {title.text}")

    # 著者を取得
    author = root.find(".//dc:creator", ns)
    if author is not None:
        print(f"著者: {author.text}")

    return {"title": title.text, "author": author.text}


def main():
    argv = sys.argv
    if len(argv) != 2:
        print("Usage: python read_ISBN.py <image_path>")
        return
    return read_ISBN_from_image(argv[1])


if __name__ == "__main__":
    main()
