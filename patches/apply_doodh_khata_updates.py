from pathlib import Path

p = Path("project/app/src/main/java/com/doodhkhata/app/MainActivity.java")
s = p.read_text()

old_base = 'void base(String title){ root=new LinearLayout(this); root.setOrientation(1); root.setBackgroundColor(Color.rgb(246,249,252)); ScrollView sc=new ScrollView(this); page=new LinearLayout(this); page.setOrientation(1); page.setPadding(dp(pad),dp(12),dp(pad),dp(28)); sc.addView(page); root.addView(sc); setContentView(root); page.addView(text("🥛 "+title,25,true)); }'
new_base = 'void base(String title){ root=new LinearLayout(this); root.setOrientation(1); root.setBackgroundColor(Color.rgb(241,247,244)); TextView header=text("🥛  DOODH KHATA",20,true); header.setTextColor(Color.WHITE); header.setGravity(Gravity.CENTER_VERTICAL); header.setPadding(dp(18),dp(18),dp(18),dp(18)); header.setBackgroundColor(Color.rgb(18,91,68)); root.addView(header); ScrollView sc=new ScrollView(this); page=new LinearLayout(this); page.setOrientation(1); page.setBackgroundColor(Color.WHITE); page.setElevation(dp(3)); page.setOrientation(1); page.setPadding(dp(pad),dp(12),dp(pad),dp(28)); sc.addView(page); LinearLayout.LayoutParams sp=new LinearLayout.LayoutParams(-1,0,1); sp.setMargins(dp(10),dp(10),dp(10),dp(10)); root.addView(sc,sp); setContentView(root); page.addView(text(title,22,true)); }'
if old_base not in s:
    raise SystemExit("Could not find expected home layout method; no changes applied.")
s = s.replace(old_base, new_base, 1)

old_msg = 'String message="*DOODH KHATA – MILK ORDER*\\n\\n*Delivery Date:* "+d+"\\n──────────────────\\nRegular Milk: "+r+" Litres\\nCow Milk: "+c+" Litres\\n──────────────────\\nPlease confirm tomorrow\'s delivery. Thank you.";\n        try{Intent i=new Intent(Intent.ACTION_VIEW,Uri.parse("https://wa.me/"+num+"?text="+android.net.Uri.encode(message))); startActivity(i);}catch(Exception e){msg("WhatsApp could not be opened");}'
new_msg = 'String message="*Regular Milk -* "+r+" L\\n*Cow Milk -* "+c+" L\\n\\nD601";\n        try{ Intent i=new Intent(Intent.ACTION_VIEW,Uri.parse("https://wa.me/"+num+"?text="+android.net.Uri.encode(message))); i.setPackage("com.whatsapp"); startActivity(i); }catch(Exception e){ msg("Please install or enable the normal WhatsApp app (not WhatsApp Business)."); }'
if old_msg not in s:
    raise SystemExit("Could not find expected WhatsApp message block; no changes applied.")
s = s.replace(old_msg, new_msg, 1)
p.write_text(s)
print("Applied Doodh Khata layout and WhatsApp order-format updates.")
