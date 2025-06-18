# ---------- Birthday Commands ------

# ------------- Constants -----------
BIRTHDAY_FILE = "birthdays.json"  # stores {"user_id": "DD-MM"}
BIRTHDAY_CHANNEL_ID = 1383512748465590326  # <- hard‑coded channel for wishes

# ------------- File Helpers --------

def load_birthdays() -> dict[str, str]:
    if os.path.exists(BIRTHDAY_FILE):
        try:
            with open(BIRTHDAY_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {}


def save_birthdays(data: dict[str, str]):
    with open(BIRTHDAY_FILE, "w") as f:
        json.dump(data, f)


birthdays = load_birthdays()

# ------------- Events --------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    if not check_birthdays.is_running():
        check_birthdays.start()
@bot.command(name="addbirthday")
async def add_birthday(ctx, member: discord.Member, date: str):
    """Save a member's birthday. Usage: !addbirthday @user DD-MM"""
    try:
        datetime.strptime(date, "%d-%m")  # validate format
    except ValueError:
        await ctx.send("❌ Invalid date format. Use DD-MM, e.g. 18-06")
        return

    birthdays[str(member.id)] = date
    save_birthdays(birthdays)
    await ctx.send(f"✅ Birthday added for {member.mention} on {date}.")


@bot.command(name="birthdays")
async def list_birthdays(ctx):
    """Show all saved birthdays."""
    if not birthdays:
        await ctx.send("No birthdays saved yet. Add one with !addbirthday @user DD-MM")
        return

    lines = ["🎂 **Saved Birthdays**:"]
    for uid, date in birthdays.items():
        user = await bot.fetch_user(int(uid))
        lines.append(f"- {user.name}: {date}")
    await ctx.send("\n".join(lines))

# --------- Background Task ---------
@tasks.loop(hours=24)
async def check_birthdays():
    today = datetime.now().strftime("%d-%m")
    for uid, date in birthdays.items():
        if date != today:
            continue
        for guild in bot.guilds:
            member = guild.get_member(int(uid))
            if not member:
                continue
            channel = guild.get_channel(BIRTHDAY_CHANNEL_ID)
            if channel and channel.permissions_for(guild.me).send_messages:
                await channel.send(
                    f"🎉 Everyone, please wish {member.mention} a **Happy Birthday!** 🥳"
                 