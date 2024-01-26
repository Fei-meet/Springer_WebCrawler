import requests
import pandas as pd

# 你的API密钥
api_key = 'User_Key'

# 定义CSV文件名
csv_file = 'data.csv'

# 每次请求的文章数量
articles_per_request = 100

# 循环获取数据，总共获取1000篇文章
for start in range(1, 1000, articles_per_request):
    url = f'http://api.springernature.com/meta/v2/json?q=year:2020&api_key={api_key}&s={start}&p={articles_per_request}'

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'records' in data:
            articles_data = []
            for record in data['records']:
                article_info = {
                    'Title': record.get('title', ''),
                    'Authors': "; ".join([author.get('creator', '') for author in record.get('creators', [])]),
                    'Abstract': record.get('abstract', ''),
                    'Publication Date': record.get('publicationDate', ''),
                    'Keywords/Tags': "; ".join(record.get('keyword', [])),
                    'Citations': record.get('citations', ''),
                    'Journal Reference': record.get('publicationName', ''),
                    'DOI': record.get('doi', ''),
                    'PDF URL': next((url['value'] for url in record.get('url', []) if url.get('format') == 'pdf'), ''),
                    'Web URL': next((url['value'] for url in record.get('url', []) if url.get('format') == 'html'), ''),
                    'Affiliations': "; ".join([affiliation for affiliation in record.get('affiliations', [])]),
                    'Page Numbers': f"{record.get('startingPage', '')}--{record.get('endingPage', '')}",
                    # 'Subject Classification': "; ".join([subject.get('term', '') for subject in record.get('subjects', [])]),
                    'Download Count': record.get('downloadCount', '')
                }
                articles_data.append(article_info)

            # 使用Pandas创建DataFrame
            df = pd.DataFrame(articles_data)

            # 以追加模式保存到CSV文件
            df.to_csv(csv_file, mode='a', index=False, header=not start > 1, encoding='utf-8-sig')

            print(f"Saved articles from start index {start}")
    else:
        print(f'Error: {response.status_code}')
        break

print("Article data saved to articles_data.csv")
