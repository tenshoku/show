import json
import os

import discord

import secret  # 個人データ

client = discord.Client()
module_dir = os.path.dirname(__file__)

# ****************************


@client.event
async def on_ready():
    print("-"*20)
    print(client.user.name)
    print("起動中")
    print("-"*20)
# ****************************


@client.event
async def on_message(message):
    key_path = os.path.join(module_dir, 'keyword.json')
    key_json_open = open(key_path, 'r', encoding="utf-8_sig")
    key_json_load = json.load(key_json_open)

    if message.content == ".set_channel":
        if message.author.bot:  # BOTの競合回避
            return
        else:
            key_json_load["list_channel"] = message.channel.id
            with open(key_path, 'w', encoding='utf-8') as f:
                json.dump(key_json_load, f, indent=4, ensure_ascii=False)
                await message.channel.send("チャンネル設定が完了しました。")

# キーワードの追加
    elif message.content.startswith(".add_keyword "):
        new_keyword = message.content[13:]
        key_json_load["キーワード"].append(new_keyword)
        with open(key_path, 'w', encoding='utf-8') as f:
            json.dump(key_json_load, f, indent=4, ensure_ascii=False)
            await message.channel.send(f"「{new_keyword}」を追加しました")

# キーワードの削除
    elif message.content.startswith(".del_keyword "):
        del_keyword = message.content[13:]
        if del_keyword in key_json_load["キーワード"]:
            key_json_load["キーワード"].remove(del_keyword)
            with open(key_path, 'w', encoding='utf-8') as f:
                json.dump(key_json_load, f, indent=4, ensure_ascii=False)
                await message.channel.send(f"「{del_keyword}」を削除しました")
        else:
            await message.channel.send("指定のキーワードは検出されませんでした。")

# キーワードリストの表示
    elif message.content == ".keyword_list":
        get_list = "\n".join(key_json_load["キーワード"])
        await message.channel.send(f"```{get_list}```")

# 自動メッセージシステム
    elif message.author.bot:
        if message.channel.id != key_json_load["list_channel"]:
            channel = client.get_channel(message.channel.id)
            msg = await channel.fetch_message(message.id)
            msg_embed = msg.embeds[0].copy()
            embed_dict = msg_embed.to_dict()
            embed_fields = embed_dict["fields"]
            channel = client.get_channel(key_json_load["list_channel"])
            for i in embed_fields:
                split_name = i["name"].split(" ")
                if "Status" in split_name:
                    secret.name_list.append("Status")
                if "Status" in i["name"]:
                    if "Out of Stock" not in i["value"]:
                        for x in key_json_load["キーワード"]:
                            if x in embed_dict["title"]:
                                await channel.send(content="@everyone", embed=msg.embeds[0].copy())
                                break
            if "Status" not in secret.name_list:
                for x in key_json_load["キーワード"]:
                            if x in embed_dict["title"]:
                                await channel.send(content="@everyone", embed=msg.embeds[0].copy())
                                break
            secret.name_list.clear()


client.run(secret.token)
