import time

import requests
from lxml import etree
import asyncio
import aiohttp
import aiofiles
import time


def get_every_chapter_url(url):
    headers ={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.58"
    }
    resp = requests.get(url,headers=headers)
    tree = etree.HTML(resp.text)
    herf_list = tree.xpath("//dl[@class='zjlist']/dd/a/@href")
    herf_lists = []
    for list in herf_list:
        herf_lists.append("https://www.bbiquge.net/book/59265/"+list)
    return herf_lists

async def download_one(url): #下载一个
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            page_source = await resp.text(encoding="gb18030")
            tree = etree.HTML(page_source)
            title = tree.xpath("//div/h1/text()")[0]
            # content = tree.xpath("//div[@id='content']/text()")
            content = "\n".join(tree.xpath("//div[@id='content']/text()")).replace("\xa0","")
            # print(title)
            async with aiofiles.open(f"./神印王座II皓月当空/{title}.txt",mode="w",encoding="utf-8") as f:
                await f.write(content)
            print("下载完毕",url)




async def download(herf_list):
    tasks = []
    for herf in herf_list:
        t = asyncio.create_task(download_one(herf))
        tasks.append(t)

    await asyncio.wait(tasks)
def main():
    url ="https://www.bbiquge.net/book/59265/"
    "https://www.bbiquge.net/book/59265/58018003.html"
    #1.拿到页面当中每一个章节的url
    herf_list = get_every_chapter_url(url)
    # print(herf_list)
    #2.启动协程,开始一节一节下载
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(download(herf_list))#运行协程任务
    # asyncio.run(download(herf_list))


if __name__ == '__main__':
    main()
