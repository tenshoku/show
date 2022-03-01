import json
import os

import discord  # discord.pyをインポート
from discord.ext import commands  # Bot Commands Frameworkのインポート

module_dir = os.path.dirname(__file__)


class TestCog(commands.Cog):

    # TestCogクラスのコンストラクタ。Botを受取り、インスタンス変数として保持。
    def __init__(self, bot):
        self.bot = bot

# 紐付け設定 /set_add *
    @commands.command()
    async def set_add(self, ctx, icon_role, auth_role, calling_name):
        path = os.path.join(module_dir, 'role.json')  # encoding="utf-8_sig"
        json_open = open(path, 'r', encoding="utf-8_sig")
        json_load = json.load(json_open)
        name_list = []

        for n in json_load:
            name_list.append(n)
        if calling_name in name_list:
            await ctx.send(f"{n}は、登録済みの名前です。")

        else:
            input_set = {calling_name: {icon_role: auth_role}}
            json_load.update(input_set)
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(json_load, f, indent=4, ensure_ascii=False)
            await ctx.send(f"{calling_name} >> {icon_role} : {auth_role} で登録しました。")

# 紐付け削除 /set_delete *
    @commands.command()
    async def set_delete(self, ctx, calling_name):
        path = os.path.join(module_dir, 'role.json')  # encoding="utf-8_sig"
        json_open = open(path, 'r', encoding="utf-8_sig")
        json_load = json.load(json_open)

        if calling_name in json_load:
            del json_load[calling_name]
            await ctx.send(f"{calling_name} を削除しました。")
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(json_load, f, indent=4, ensure_ascii=False)
        else:
            await ctx.send("登録されていないか、入力を間違えています。")

# 紐付け情報の表示 /set_list
    @commands.command()
    async def set_list(self, ctx):
        path = os.path.join(module_dir, 'role.json')  # encoding="utf-8_sig"
        json_open = open(path, 'r', encoding="utf-8_sig")
        json_load = json.load(json_open)
        array = []

        for setkey, setrole in json_load.items():
            for rolekey, roleval in setrole.items():
                array.append(f"{setkey}   >>   {rolekey} :   {roleval}")

        embed = discord.Embed(title="__設定済みロールリスト__", color=0x04ff00)

        for n in array:
            embed.add_field(name=f"{n}", value="-", inline=False)
        await ctx.send(embed=embed)

# ユーザーが紐付け情報からロールを取得 /get *
    @commands.command()
    async def get(self, ctx, calling_name):
        path = os.path.join(module_dir, 'role.json')  # encoding="utf-8_sig"
        json_open = open(path, 'r', encoding="utf-8_sig")
        json_load = json.load(json_open)

        name_list = []
        icon_role_list = []
        member = ctx.message.author

        for keys in json_load:
            name_list.append(keys)
            for k in json_load[keys].keys():
                icon_role_list.append(k)

        if calling_name in name_list:
            ar = list(json_load[calling_name].values())
            ai = list(json_load[calling_name].keys())
            auth_role = ar[0]  # 認証ロールのstr
            icon_role = ai[0]  # アイコンロールのstr

            a_role = discord.utils.get(self.bot.get_guild(
                ctx.guild.id).roles, name=auth_role)  # DISCORDに渡す形式に変換 auth_role

            if a_role in member.roles:
                i_role = discord.utils.get(self.bot.get_guild(
                    ctx.guild.id).roles, name=icon_role)  # icon_role

                # 他のアイコンロールをすべて削除
                icon_role_list.remove(icon_role)
                for del_role in icon_role_list:
                    remove_role = discord.utils.get(self.bot.get_guild(
                        ctx.guild.id).roles, name=del_role)  # del_role

                    await member.remove_roles(remove_role)

                # 指定したアイコンロールを登録
                await member.add_roles(i_role)
                await ctx.message.delete()

            else:
                await ctx.message.delete()
        else:
            await ctx.message.delete()

# ユーザーが取得可能なロールの表示 /get_list
    @commands.command()
    async def get_list(self, ctx):
        path = os.path.join(module_dir, 'role.json')  # encoding="utf-8_sig"
        json_open = open(path, 'r', encoding="utf-8_sig")
        json_load = json.load(json_open)

        member = ctx.message.author
        has_roles = []
        ok_roles = []

        for role in member.roles:
            has_roles.append(role.name)  # 入力者のロールデータ取得

        for k, v in json_load.items():  # 登録データから表示可能なアイコンリストの取得
            for ir, ar in v.items():
                if ar in has_roles:
                    ok_roles.append(k)

        embed = discord.Embed(title="↓取得可能！")
        for r in ok_roles:
            embed.add_field(name=f"{r} ", value="＿＿＿＿＿", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(TestCog(bot))
