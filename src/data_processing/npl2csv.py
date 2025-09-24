import pandas as pd
import os

def convert_qry_to_csv(input_file, output_file):
    queries = []
    current_query_id = None
    current_text = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '/':  # پایان پرس‌وجو
                if current_query_id is not None and current_text:
                    queries.append({'QueryID': current_query_id, 'Text': ' '.join(current_text).strip()})
                    current_text = []
                    current_query_id = None
                continue
            if not line:
                continue
            if line.isdigit():  # خط شامل QueryID
                if current_query_id is not None and current_text:
                    queries.append({'QueryID': current_query_id, 'Text': ' '.join(current_text).strip()})
                    current_text = []
                current_query_id = int(line)
            else:  # خط شامل متن پرس‌وجو
                current_text.append(line)
    
    # افزودن آخرین پرس‌وجو (اگر وجود داشته باشد)
    if current_query_id is not None and current_text:
        queries.append({'QueryID': current_query_id, 'Text': ' '.join(current_text).strip()})
    
    # تبدیل به DataFrame و ذخیره به CSV
    if queries:
        df = pd.DataFrame(queries)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Queries saved to {output_file}")
    else:
        print(f"No queries found in {input_file}")

def convert_all_to_csv(input_file, output_file):
    docs = []
    current_doc_id = None
    current_text = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '/':  # پایان سند
                if current_doc_id is not None and current_text:
                    docs.append({'DocID': current_doc_id, 'Text': ' '.join(current_text).strip()})
                    current_text = []
                    current_doc_id = None
                continue
            if not line:
                continue
            if line.isdigit():  # خط شامل DocID
                if current_doc_id is not None and current_text:
                    docs.append({'DocID': current_doc_id, 'Text': ' '.join(current_text).strip()})
                    current_text = []
                current_doc_id = int(line)
            else:  # خط شامل متن سند
                current_text.append(line)
    
    # افزودن آخرین سند (اگر وجود داشته باشد)
    if current_doc_id is not None and current_text:
        docs.append({'DocID': current_doc_id, 'Text': ' '.join(current_text).strip()})
    
    # تبدیل به DataFrame و ذخیره به CSV
    if docs:
        df = pd.DataFrame(docs)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Documents saved to {output_file}")
    else:
        print(f"No documents found in {input_file}")

def convert_rel_to_csv(input_file, output_file):
    qrels = []
    current_query_id = None
    current_doc_ids = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line == '/':  # پایان گروه
                if current_query_id is not None and current_doc_ids:
                    for doc_id in current_doc_ids:
                        qrels.append({'QueryID': current_query_id, 'DocID': doc_id, 'Relevance': 1})
                    current_query_id = None
                    current_doc_ids = []
                continue
            if not line:
                continue
            parts = line.split()
            if not parts:
                continue
            if parts[0].isdigit() and current_query_id is None:  # خط شامل QueryID
                current_query_id = int(parts[0])
                current_doc_ids.extend(int(doc_id) for doc_id in parts[1:] if doc_id.isdigit())
            elif current_query_id is not None:  # خط شامل DocIDهای اضافی
                current_doc_ids.extend(int(doc_id) for doc_id in parts if doc_id.isdigit())
    
    # افزودن آخرین گروه (اگر وجود داشته باشد)
    if current_query_id is not None and current_doc_ids:
        for doc_id in current_doc_ids:
            qrels.append({'QueryID': current_query_id, 'DocID': doc_id, 'Relevance': 1})
    
    # تبدیل به DataFrame و ذخیره به CSV
    if qrels:
        df = pd.DataFrame(qrels)
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Qrels saved to {output_file}")
    else:
        print(f"No qrelsRos found in {input_file}")

if __name__ == "__main__":
    base_path = './collections'
    os.makedirs(base_path, exist_ok=True)
    
    # مسیر فایل‌های ورودی
    qry_file = './collections/NPL/npl.QRY'
    all_file = './collections/NPL/npl.ALL'
    rel_file = './collections/NPL/npl.REL'
    
    # مسیر فایل‌های خروجی
    queries_csv = os.path.join(base_path, 'npl_queries.csv')
    docs_csv = os.path.join(base_path, 'npl_docs.csv')
    qrels_csv = os.path.join(base_path, 'npl_qrels.csv')
    
    # تبدیل فایل‌ها
    convert_qry_to_csv(qry_file, queries_csv)
    convert_all_to_csv(all_file, docs_csv)
    convert_rel_to_csv(rel_file, qrels_csv)