from pathlib import Path
import re
p=Path("project/app/src/main/java/com/doodhkhata/app/MainActivity.java")
s=p.read_text()
s=s.replace('TextView summary; String blue="#1976D2"; int pad=16;','TextView summary, deliveryDateView; String blue="#1976D2"; String selectedDeliveryDate; int pad=16;')
s=s.replace('Button button(String s,Runnable r){ Button b=new Button(this); b.setText(s); b.setAllCaps(false); b.setOnClickListener(v->r.run()); return b; }','Button button(String s,Runnable r){ Button b=new Button(this); b.setText(s); b.setAllCaps(false); b.setTextColor(Color.WHITE); if(android.os.Build.VERSION.SDK_INT>=21)b.setBackgroundTintList(android.content.res.ColorStateList.valueOf(Color.rgb(24,112,82))); b.setPadding(dp(14),dp(10),dp(14),dp(10)); LinearLayout.LayoutParams lp=new LinearLayout.LayoutParams(-1,-2); lp.setMargins(0,dp(5),0,dp(5)); b.setLayoutParams(lp); b.setOnClickListener(v->r.run()); return b; }')
old='void base(String title){ root=new LinearLayout(this); root.setOrientation(1); root.setBackgroundColor(Color.rgb(246,249,252)); ScrollView sc=new ScrollView(this); page=new LinearLayout(this); page.setOrientation(1); page.setPadding(dp(pad),dp(12),dp(pad),dp(28)); sc.addView(page); root.addView(sc); setContentView(root); page.addView(text("🥛 "+title,25,true)); }'
new='void base(String title){ root=new LinearLayout(this); root.setOrientation(1); root.setBackgroundColor(Color.rgb(238,246,241)); TextView header=text("🥛  DOODH KHATA",21,true); header.setTextColor(Color.WHITE); header.setGravity(Gravity.CENTER_VERTICAL); header.setPadding(dp(20),dp(20),dp(20),dp(20)); header.setBackgroundColor(Color.rgb(18,91,68)); root.addView(header); ScrollView sc=new ScrollView(this); page=new LinearLayout(this); page.setOrientation(1); page.setBackgroundColor(Color.WHITE); page.setElevation(dp(3)); page.setPadding(dp(pad),dp(16),dp(pad),dp(28)); sc.addView(page); LinearLayout.LayoutParams sp=new LinearLayout.LayoutParams(-1,0,1); sp.setMargins(dp(10),dp(10),dp(10),dp(10)); root.addView(sc,sp); setContentView(root); page.addView(text(title,22,true)); }'
if old in s:s=s.replace(old,new,1)
elif '🥛  DOODH KHATA' not in s:raise SystemExit('Base layout not found')
old='page.addView(text("Daily milk order · Delivery date: "+todayPlus(1),16,true));'
new='selectedDeliveryDate=selectedDeliveryDate==null?todayPlus(1):selectedDeliveryDate; page.addView(text("MILK ORDER",13,true)); deliveryDateView=text("Delivery date: "+selectedDeliveryDate,17,true); page.addView(deliveryDateView); page.addView(button("📅 Change delivery date",()->chooseDeliveryDate()));'
if old in s:s=s.replace(old,new,1)
elif 'chooseDeliveryDate()' not in s:raise SystemExit('Home date line not found')
s=s.replace('page.addView(button("SAVE TOMORROW\'S ORDER",()->saveOrder()));','page.addView(button("SAVE MILK ORDER",()->saveOrder()));')
if 'void chooseDeliveryDate()' not in s:
 a='    void saveOrder(){'
 m='''    void chooseDeliveryDate(){ try{ Calendar cal=Calendar.getInstance(); if(selectedDeliveryDate==null)selectedDeliveryDate=todayPlus(1); Date parsed=new SimpleDateFormat("yyyy-MM-dd",Locale.US).parse(selectedDeliveryDate); if(parsed!=null)cal.setTime(parsed); new DatePickerDialog(this,(view,year,month,day)->{ Calendar chosen=Calendar.getInstance(); chosen.set(year,month,day); selectedDeliveryDate=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(chosen.getTime()); if(deliveryDateView!=null)deliveryDateView.setText("Delivery date: "+selectedDeliveryDate); },cal.get(Calendar.YEAR),cal.get(Calendar.MONTH),cal.get(Calendar.DAY_OF_MONTH)).show(); }catch(Exception e){msg("Could not open date picker");} }
'''
 if a not in s:raise SystemExit('saveOrder not found')
 s=s.replace(a,m+a,1)
s=s.replace('SQLiteDatabase w=db.getWritableDatabase(); String d=todayPlus(1);','SQLiteDatabase w=db.getWritableDatabase(); String d=selectedDeliveryDate==null?todayPlus(1):selectedDeliveryDate;')
s=s.replace('String d=todayPlus(1), num=setting("phone","918976628887").replaceAll("[^0-9]","");','String d=selectedDeliveryDate==null?todayPlus(1):selectedDeliveryDate, num=setting("phone","918976628887").replaceAll("[^0-9]","");')
pattern=r'String message=.*?;\s*try\{Intent i=new Intent\(Intent\.ACTION_VIEW,Uri\.parse\("https://wa\.me/"\+num\+"\?text="\+android\.net\.Uri\.encode\(message\)\)\);.*?\}\s*catch\(Exception e\)\{msg\("WhatsApp could not be opened"\);\}'
replacement='''String message="*Delivery Date:* "+d+"\\n\\n*Regular Milk -* "+r+" L\\n*Cow Milk -* "+c+" L\\n\\nD601";
        try{Intent i=new Intent(Intent.ACTION_VIEW,Uri.parse("https://wa.me/"+num+"?text="+android.net.Uri.encode(message))); i.setPackage("com.whatsapp"); startActivity(i);}catch(Exception e){msg("Please install or enable the normal WhatsApp app (not WhatsApp Business).");}'''
s2,n=re.subn(pattern,lambda m:replacement,s,count=1,flags=re.S)
if n:s=s2
elif 'String message="*Delivery Date:* "' not in s:raise SystemExit('WhatsApp block not found')
old='''box.addView(er);box.addView(ec);box.addView(sp);
        new AlertDialog.Builder(this).setTitle("Edit "+d).setView(box).setPositiveButton("Save",(x,y)->{
            try{ContentValues v=new ContentValues();v.put("reg_qty",Double.parseDouble(er.getText().toString()));v.put("cow_qty",Double.parseDouble(ec.getText().toString()));v.put("payment",sp.getSelectedItem().toString());db.getWritableDatabase().update("orders",v,"date=?",new String[]{d});showBills();}catch(Exception e){msg("Invalid quantity");}
        }).setNegativeButton("Cancel",null).show();'''
new='''final String[] editedDate={d}; TextView dateText=text("Delivery date: "+d,15,true); box.addView(dateText); box.addView(button("Change delivery date",()->{ try{Calendar cal=Calendar.getInstance();Date parsed=new SimpleDateFormat("yyyy-MM-dd",Locale.US).parse(editedDate[0]);if(parsed!=null)cal.setTime(parsed);new DatePickerDialog(this,(view,year,month,day)->{Calendar chosen=Calendar.getInstance();chosen.set(year,month,day);editedDate[0]=new SimpleDateFormat("yyyy-MM-dd",Locale.US).format(chosen.getTime());dateText.setText("Delivery date: "+editedDate[0]);},cal.get(Calendar.YEAR),cal.get(Calendar.MONTH),cal.get(Calendar.DAY_OF_MONTH)).show();}catch(Exception e){msg("Could not open date picker");} })); box.addView(er);box.addView(ec);box.addView(sp);
        new AlertDialog.Builder(this).setTitle("Edit order").setView(box).setPositiveButton("Save",(x,y)->{try{ContentValues v=new ContentValues();v.put("date",editedDate[0]);v.put("reg_qty",Double.parseDouble(er.getText().toString()));v.put("cow_qty",Double.parseDouble(ec.getText().toString()));v.put("payment",sp.getSelectedItem().toString());int changed=db.getWritableDatabase().update("orders",v,"date=?",new String[]{d});if(changed==0)msg("Order could not be updated");showBills();}catch(Exception e){msg("Invalid details or an order already exists for that date");}}).setNegativeButton("Cancel",null).show();'''
if old in s:s=s.replace(old,new,1)
elif 'final String[] editedDate={d};' not in s:raise SystemExit('Edit dialog block not found')
p.write_text(s)
print("Applied modern layout and manual delivery-date selection/editing.")
