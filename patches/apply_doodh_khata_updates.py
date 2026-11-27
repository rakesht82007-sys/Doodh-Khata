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


# Create a modern Doodh Khata launcher icon (milk bottle + fresh green branding).
res = Path("project/app/src/main/res")
drawable = res / "drawable"
drawable.mkdir(parents=True, exist_ok=True)
icon = """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp"
    android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#0F6B4F"
        android:pathData="M18,0 L90,0 Q108,0 108,18 L108,90 Q108,108 90,108 L18,108 Q0,108 0,90 L0,18 Q0,0 18,0 Z"/>
    <path android:fillColor="#FFFFFF"
        android:pathData="M43,19 L65,19 L65,29 L72,38 L72,82 Q72,88 66,88 L42,88 Q36,88 36,82 L36,38 L43,29 Z"/>
    <path android:fillColor="#D8F3E6"
        android:pathData="M43,19 L65,19 L65,28 L43,28 Z"/>
    <path android:fillColor="#29A879"
        android:pathData="M39,55 L69,55 L69,79 Q69,84 64,84 L44,84 Q39,84 39,79 Z"/>
    <path android:fillColor="#FFFFFF"
        android:pathData="M54,59 C49,66 47,69 47,72 C47,76 50,79 54,79 C58,79 61,76 61,72 C61,69 59,66 54,59 Z"/>
    <path android:fillColor="#B8E8D3"
        android:pathData="M44,35 L64,35 L68,41 L40,41 Z"/>
</vector>
"""
(drawable / "ic_launcher.xml").write_text(icon)
manifest = Path("project/app/src/main/AndroidManifest.xml")
m = manifest.read_text()
if 'android:icon="@drawable/ic_launcher"' not in m:
    m = m.replace('android:label="Doodh Khata"', 'android:label="Doodh Khata" android:icon="@drawable/ic_launcher"')
manifest.write_text(m)
print("Added the Doodh Khata launcher icon.")


# Replace the monthly PDF export with a properly aligned table and a final total row.
main = Path("project/app/src/main/java/com/doodhkhata/app/MainActivity.java")
java = main.read_text()
pdf_method = r"""    void exportPdf(String m){
        PdfDocument pdf=new PdfDocument();
        Cursor cur=null;
        try{
            cur=db.getReadableDatabase().rawQuery("SELECT date,reg_qty,cow_qty,payment FROM orders WHERE date LIKE ? ORDER BY date",new String[]{m+"%"});
            final int left=35, right=560, rowH=25;
            final int[] x={35,112,178,244,310,376,465,560};
            Paint p=new Paint(3);
            p.setColor(Color.BLACK);
            int pageNo=1, y=0;
            PdfDocument.Page pg=null;
            Canvas canvas=null;
            double total=0;
            int rows=0;
            java.text.DecimalFormat qtyFmt=new java.text.DecimalFormat("0.##");
            Runnable startPage=()->{};
            // Page creation and table header are repeated whenever the table continues.
            while(cur.moveToNext()){
                if(pg==null || y>755){
                    if(pg!=null)pdf.finishPage(pg);
                    PdfDocument.PageInfo info=new PdfDocument.PageInfo.Builder(595,842,pageNo++).create();
                    pg=pdf.startPage(info); canvas=pg.getCanvas();
                    p.setColor(Color.rgb(18,91,68)); p.setTextSize(19); p.setTypeface(android.graphics.Typeface.create("sans-serif",android.graphics.Typeface.BOLD));
                    canvas.drawText("DOODH KHATA - MONTHLY MILK BILL",left,42,p);
                    p.setColor(Color.DKGRAY); p.setTextSize(11); p.setTypeface(android.graphics.Typeface.create("sans-serif",0));
                    canvas.drawText("Month: "+m+"     Date-wise bill statement",left,65,p);
                    y=91;
                    p.setColor(Color.rgb(224,239,230)); canvas.drawRect(left,y,right,y+rowH,p);
                    p.setColor(Color.rgb(18,91,68)); p.setTextSize(9); p.setTypeface(android.graphics.Typeface.create("sans-serif",android.graphics.Typeface.BOLD));
                    String[] heads={"Date","Reg Qty","Reg Rate","Cow Qty","Cow Rate","Amount","Payment"};
                    for(int i=0;i<heads.length;i++)canvas.drawText(heads[i],x[i]+4,y+16,p);
                    p.setColor(Color.GRAY); p.setStrokeWidth(0.7f); canvas.drawLine(left,y+rowH,right,y+rowH,p);
                    y+=rowH;
                }
                String d=cur.getString(0);
                double r=cur.getDouble(1), co=cur.getDouble(2);
                double[] rt=rates(d);
                double amt=r*rt[0]+co*rt[1];
                total+=amt; rows++;
                p.setTypeface(android.graphics.Typeface.create("sans-serif",0)); p.setTextSize(9); p.setColor(Color.BLACK);
                String[] vals={d,qtyFmt.format(r),money(rt[0]),qtyFmt.format(co),money(rt[1]),money(amt),cur.getString(3)};
                for(int i=0;i<vals.length;i++){
                    String v=vals[i]==null?"":vals[i];
                    float max=x[i+1]-x[i]-7;
                    while(p.measureText(v)>max && v.length()>3)v=v.substring(0,v.length()-1);
                    if(!v.equals(vals[i]))v=v+"…";
                    canvas.drawText(v,x[i]+4,y+16,p);
                }
                p.setColor(Color.LTGRAY); p.setStrokeWidth(0.5f); canvas.drawLine(left,y+rowH,right,y+rowH,p);
                y+=rowH;
            }
            cur.close(); cur=null;
            if(pg==null){
                PdfDocument.PageInfo info=new PdfDocument.PageInfo.Builder(595,842,1).create();
                pg=pdf.startPage(info); canvas=pg.getCanvas();
                p.setColor(Color.rgb(18,91,68)); p.setTextSize(19); p.setTypeface(android.graphics.Typeface.create("sans-serif",android.graphics.Typeface.BOLD));
                canvas.drawText("DOODH KHATA - MONTHLY MILK BILL",left,42,p);
                p.setColor(Color.DKGRAY); p.setTextSize(11); p.setTypeface(android.graphics.Typeface.create("sans-serif",0));
                canvas.drawText("Month: "+m+"     No orders recorded",left,65,p);
                y=91;
                p.setColor(Color.rgb(224,239,230)); canvas.drawRect(left,y,right,y+rowH,p);
                p.setColor(Color.rgb(18,91,68)); p.setTextSize(9); p.setTypeface(android.graphics.Typeface.create("sans-serif",android.graphics.Typeface.BOLD));
                String[] heads={"Date","Reg Qty","Reg Rate","Cow Qty","Cow Rate","Amount","Payment"};
                for(int i=0;i<heads.length;i++)canvas.drawText(heads[i],x[i]+4,y+16,p);
                y+=rowH;
            }
            // Keep the grand total together at the bottom of the final page.
            if(y>770){
                pdf.finishPage(pg);
                PdfDocument.PageInfo info=new PdfDocument.PageInfo.Builder(595,842,pageNo++).create();
                pg=pdf.startPage(info); canvas=pg.getCanvas();
                p.setColor(Color.rgb(18,91,68)); p.setTextSize(19); p.setTypeface(android.graphics.Typeface.create("sans-serif",android.graphics.Typeface.BOLD));
                canvas.drawText("DOODH KHATA - MONTHLY MILK BILL",left,42,p);
                p.setColor(Color.DKGRAY); p.setTextSize(11); p.setTypeface(android.graphics.Typeface.create("sans-serif",0));
                canvas.drawText("Month: "+m+"     Continued",left,65,p);
                y=100;
            }
            p.setColor(Color.rgb(224,239,230)); canvas.drawRect(left,y,right,y+30,p);
            p.setColor(Color.rgb(18,91,68)); p.setTextSize(13); p.setTypeface(android.graphics.Typeface.create("sans-serif",android.graphics.Typeface.BOLD));
            canvas.drawText("TOTAL BILL ("+rows+" orders)",left+8,y+20,p);
            canvas.drawText(money(total),right-95,y+20,p);
            p.setColor(Color.DKGRAY); p.setTextSize(9); p.setTypeface(android.graphics.Typeface.create("sans-serif",0));
            canvas.drawText("Generated by Doodh Khata",left,815,p);
            pdf.finishPage(pg); pg=null;
            File f=new File(getExternalFilesDir(null),"DoodhKhata-"+m+".pdf");
            FileOutputStream os=new FileOutputStream(f); pdf.writeTo(os); os.close(); pdf.close();
            shareFile(f,"application/pdf");
        }catch(Exception e){
            if(cur!=null)cur.close();
            try{pdf.close();}catch(Exception ignored){}
            msg("PDF export failed: "+e.getMessage());
        }
    }
"""
pattern=r"    void exportPdf\(String m\)\{.*?\n    \}\n    void shareFile"
java2,n=re.subn(pattern,lambda _:pdf_method+"\n    void shareFile",java,count=1,flags=re.S)
if n!=1:
    raise SystemExit("Could not locate the existing exportPdf method; refusing to alter the build.")
main.write_text(java2)
print("Updated monthly PDF export to a date-wise table with a grand total.")


# Add a dedicated all-records screen so every saved milk entry can be reviewed and edited.
main = Path("project/app/src/main/java/com/doodhkhata/app/MainActivity.java")
java = main.read_text()
old_menu = 'page.addView(button("Monthly bill & date-wise records",()->showBills()));'
new_menu = old_menu + '\n        page.addView(button("Edit all saved records",()->showAllRecords()));'
if 'showAllRecords()' not in java:
    if old_menu not in java:
        raise SystemExit("Could not find the monthly records menu to add the Records screen.")
    java = java.replace(old_menu, new_menu, 1)
    marker = '    void showCharts(){'
    method = '''    void showAllRecords(){
        base("All saved records");
        page.addView(text("Edit any saved date, milk quantity or payment status. Changes are saved to your database.",14,false));
        Cursor c=db.getReadableDatabase().rawQuery("SELECT date,reg_qty,cow_qty,payment FROM orders ORDER BY date DESC",null);
        int count=0;
        while(c.moveToNext()){
            String d=c.getString(0); double r=c.getDouble(1), co=c.getDouble(2); String pay=c.getString(3);
            double[] rt=rates(d); double amount=r*rt[0]+co*rt[1];
            page.addView(text(d+"\\nRegular: "+r+" L   |   Cow: "+co+" L\\nBill: "+money(amount)+"   |   "+pay,15,true));
            final String date=d; final double rq=r,cq=co; final String payment=pay;
            page.addView(button("EDIT / SAVE THIS RECORD",()->editEntry(date,rq,cq,payment)));
            page.addView(button("DELETE THIS DAY'S RECORD",()->new AlertDialog.Builder(MainActivity.this)
                .setTitle("Delete record?")
                .setMessage("Are you sure you want to Delete this day's record?")
                .setNegativeButton("Cancel",(dialog,which)->dialog.dismiss())
                .setPositiveButton("Delete",(dialog,which)->{
                    db.getWritableDatabase().delete("orders","date=?",new String[]{date});
                    msg("Record deleted successfully.");
                    showAllRecords();
                }).show()));
            count++;
        }
        c.close();
        if(count==0)page.addView(text("No saved records yet.",15,false));
        page.addView(button("Back to Home",()->showHome()));
    }
'''
    if marker not in java:
        raise SystemExit("Could not find the chart screen insertion point.")
    java = java.replace(marker, method + marker, 1)
    main.write_text(java)
    print("Added an all-records editor with saved edits.")
else:
    print("All-records editor already present; no duplicate added.")
