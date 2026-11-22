package com.echo.beyond;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Paint;
import android.graphics.RectF;
import android.view.MotionEvent;
import android.view.View;
import android.os.SystemClock;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class GameView extends View {
    private final Paint p = new Paint(3);
    private final int[][] map = {
        {1,1,1,1,1,1,1,1,1,1,1,1,1,1},
        {1,0,0,0,0,0,0,0,0,0,0,0,0,1},
        {1,0,1,1,0,0,1,0,0,1,1,0,0,1},
        {1,0,0,1,0,0,1,0,0,0,1,0,0,1},
        {1,0,0,1,0,0,0,0,1,0,0,0,0,1},
        {1,0,0,0,0,1,0,0,1,0,1,1,0,1},
        {1,1,0,0,0,1,0,0,0,0,0,1,0,1},
        {1,0,0,1,0,0,0,1,1,0,0,0,0,1},
        {1,0,0,1,0,0,0,0,0,0,1,0,0,1},
        {1,0,1,1,1,0,1,0,0,0,1,0,0,1},
        {1,0,0,0,0,0,1,0,1,0,0,0,0,1},
        {1,0,0,0,0,0,0,0,0,0,0,0,0,1},
        {1,1,1,1,1,1,1,1,1,1,1,1,1,1}
    };
    private double px=1.7, py=1.7, angle=0.15;
    private float joyX, joyY, lookDelta;
    private int shards=0, hp=100, echoTicks=0, pulseTicks=0;
    private boolean started=false, won=false;
    private long lastFrame=0;
    private final List<Enemy> enemies = new ArrayList<>();
    private final List<Shard> pickups = new ArrayList<>();
    private int leftPointer=-1, lookPointer=-1;
    private float leftBaseX, leftBaseY, leftNowX, leftNowY, lastLookX;
    private float screenW, screenH;
    private final Random rng = new Random(12);

    private static class Enemy { double x,y; int stun=0; Enemy(double a,double b){x=a;y=b;} }
    private static class Shard { double x,y; boolean taken=false; Shard(double a,double b){x=a;y=b;} }

    public GameView(Context c) {
        super(c);
        setLayerType(View.LAYER_TYPE_HARDWARE, null);
        enemies.add(new Enemy(8.5,2.5));
        enemies.add(new Enemy(10.5,7.5));
        enemies.add(new Enemy(4.5,10.5));
        pickups.add(new Shard(5.5,1.7));
        pickups.add(new Shard(8.5,8.5));
        pickups.add(new Shard(11.5,10.5));
    }

    public void pauseGame(){ }
    public void resumeGame(){ lastFrame=SystemClock.uptimeMillis(); invalidate(); }

    private int color(int r,int g,int b){ return 0xff000000 | (r<<16) | (g<<8) | b; }
    private void fill(Canvas c,float l,float t,float r,float b,int col){
        p.setColor(col); p.setStyle(Paint.Style.FILL); c.drawRect(l,t,r,b,p);
    }
    private boolean solid(double x,double y){
        int mx=(int)Math.floor(x), my=(int)Math.floor(y);
        return my<0||my>=map.length||mx<0||mx>=map[0].length||map[my][mx]!=0;
    }
    private void drawText(Canvas c,String s,float x,float y,float size,int col){
        p.setColor(col); p.setTextSize(size); p.setTypeface(android.graphics.Typeface.create("sans-serif",1));
        c.drawText(s,x,y,p);
    }

    @Override protected void onDraw(Canvas c) {
        super.onDraw(c);
        screenW=getWidth(); screenH=getHeight();
        if(screenW<=0||screenH<=0)return;
        if(!started){ drawTitle(c); postInvalidateDelayed(16); return; }
        long now=SystemClock.uptimeMillis();
        float dt=lastFrame==0?0.016f:Math.min(0.05f,(now-lastFrame)/1000f);
        lastFrame=now;
        update(dt);
        renderWorld(c);
        renderHud(c);
        if(won){ fill(c,0,0,screenW,screenH,0x99000000); drawText(c,"МАЯК АКТИВИРОВАН",screenW*.30f,screenH*.48f,screenH*.065f,0xffb9ffe8); drawText(c,"ЭХО ОТКЛИКНУЛОСЬ...",screenW*.35f,screenH*.57f,screenH*.03f,0xffffffff); }
        postInvalidateDelayed(16);
    }

    private void drawTitle(Canvas c){
        fill(c,0,0,screenW,screenH,0xff07151a);
        p.setShader(new android.graphics.RadialGradient(screenW*.5f,screenH*.48f,screenH*.75f,
                new int[]{0xff24564e,0xff102b32,0xff050d13},null,android.graphics.Shader.TileMode.CLAMP));
        c.drawRect(0,0,screenW,screenH,p); p.setShader(null);
        drawText(c,"ЭХО",screenW*.405f,screenH*.37f,screenH*.16f,0xffd5fff2);
        drawText(c,"ЗА ГРАНЬЮ",screenW*.405f,screenH*.44f,screenH*.045f,0xff9bc9c0);
        drawText(c,"НАЙДИ 3 ОСКОЛКА И ДОЙДИ ДО МАЯКА",screenW*.30f,screenH*.63f,screenH*.027f,0xffd2e7df);
        p.setColor(0xff80d9bf); c.drawRoundRect(new RectF(screenW*.39f,screenH*.72f,screenW*.61f,screenH*.84f),18,18,p);
        drawText(c,"НАЧАТЬ",screenW*.455f,screenH*.795f,screenH*.035f,0xff09201d);
        drawText(c,"Левый стик — движение   •   Правая сторона — обзор",screenW*.27f,screenH*.94f,screenH*.022f,0xff9db9b4);
    }

    private void update(float dt){
        if(won)return;
        if(echoTicks>0)echoTicks--;
        if(pulseTicks>0)pulseTicks--;
        double speed=2.4*dt;
        double forward=(-joyY)*speed, strafe=joyX*speed;
        double nx=px+Math.cos(angle)*forward-Math.sin(angle)*strafe;
        double ny=py+Math.sin(angle)*forward+Math.cos(angle)*strafe;
        if(!solid(nx,py))px=nx;
        if(!solid(px,ny))py=ny;
        lookDelta=0;
        for(Shard s:pickups){
            if(!s.taken && dist(px,py,s.x,s.y)<0.55){s.taken=true;shards++;}
        }
        for(Enemy e:enemies){
            if(e.stun>0){e.stun--;continue;}
            double d=dist(px,py,e.x,e.y);
            if(d<7 && d>0.6){
                double vx=(px-e.x)/d, vy=(py-e.y)/d;
                double ex=e.x+vx*dt*.55, ey=e.y+vy*dt*.55;
                if(!solid(ex,e.y))e.x=ex;
                if(!solid(e.x,ey))e.y=ey;
            }
            if(d<0.55)hp=Math.max(0,hp-1);
        }
        if(shards>=3 && dist(px,py,11.4,11.3)<1.0)won=true;
    }
    private double dist(double x,double y,double a,double b){return Math.hypot(x-a,y-b);}

    private void renderWorld(Canvas c){
        float horizon=screenH*.49f;
        fill(c,0,0,screenW,horizon,0xff142b31);
        p.setShader(new android.graphics.LinearGradient(0,horizon,0,screenH,0xff30443b,0xff111d1a,android.graphics.Shader.TileMode.CLAMP));
        c.drawRect(0,horizon,screenW,screenH,p);p.setShader(null);
        p.setColor(0x553b8e77); c.drawCircle(screenW*.72f,screenH*.26f,screenH*.18f,p);
        int rays=(int)(screenW/3);
        double fov=Math.PI/2.7;
        for(int i=0;i<rays;i++){
            double ra=angle-fov/2+fov*i/rays;
            double rx=Math.cos(ra), ry=Math.sin(ra);
            double d=0.03;
            while(d<14 && !solid(px+rx*d,py+ry*d))d+=0.035;
            double corrected=d*Math.cos(ra-angle);
            float wallH=(float)Math.min(screenH*1.8,screenH*.82/(corrected+.12));
            float x=i*screenW/rays;
            float shade=(float)Math.max(.18,1.0-corrected/12.0);
            int base=(int)(105*shade);
            int col=color((int)(base*.72),(int)(base*1.18),(int)(base*.92));
            fill(c,x,horizon-wallH/2,x+screenW/rays+1,horizon+wallH/2,col);
            float fog=(float)Math.min(.68,corrected/18);
            fill(c,x,horizon-wallH/2,x+screenW/rays+1,horizon+wallH/2,((int)(fog*130)<<24)|0xff152b2c);
        }
        for(Shard s:pickups)if(!s.taken)drawBillboard(c,s.x,s.y,0xff75ffe1,0);
        drawBillboard(c,11.4,11.3,shards>=3?0xffffd77a:0xff5a7b73,1);
        for(Enemy e:enemies)drawBillboard(c,e.x,e.y,e.stun>0?0xffa9fff1:0xffb65d53,2);
        p.setShader(new android.graphics.RadialGradient(screenW*.5f,screenH*.5f,screenW*.7f,
                new int[]{0x00000000,0x88000000},null,android.graphics.Shader.TileMode.CLAMP));
        c.drawRect(0,0,screenW,screenH,p);p.setShader(null);
    }

    private void drawBillboard(Canvas c,double x,double y,int col,int type){
        double dx=x-px,dy=y-py, d=Math.hypot(dx,dy);
        double a=Math.atan2(dy,dx)-angle;
        while(a>Math.PI)a-=Math.PI*2; while(a<-Math.PI)a+=Math.PI*2;
        if(Math.abs(a)>0.85||d<.2)return;
        float sx=(float)(screenW*.5+Math.tan(a)*screenW*.48);
        float size=(float)Math.min(screenH*.65,screenH*.55/(d+.25));
        float sy=screenH*.49f;
        if(type==0){
            p.setColor(0x5574ffe0);c.drawCircle(sx,sy,size*.34f,p);
            p.setColor(col);c.drawCircle(sx,sy,size*.13f,p);
            p.setStyle(Paint.Style.STROKE);p.setStrokeWidth(Math.max(2,size*.025f));c.drawCircle(sx,sy,size*.22f,p);p.setStyle(Paint.Style.FILL);
        }else if(type==1){
            p.setColor(col);c.drawRect(sx-size*.12f,sy-size*.48f,sx+size*.12f,sy+size*.48f,p);
            c.drawCircle(sx,sy-size*.52f,size*.2f,p);
            p.setColor(0x6678e8ce);c.drawCircle(sx,sy,size*.55f,p);
        }else{
            p.setColor(0x553b0000);c.drawOval(sx-size*.35f,sy+size*.32f,sx+size*.35f,sy+size*.5f,p);
            p.setColor(col);c.drawRoundRect(new RectF(sx-size*.23f,sy-size*.38f,sx+size*.23f,sy+size*.4f),size*.16f,size*.16f,p);
            p.setColor(0xffffd9a4);c.drawCircle(sx-size*.09f,sy-size*.17f,size*.035f,p);c.drawCircle(sx+size*.09f,sy-size*.17f,size*.035f,p);
        }
    }

    private void renderHud(Canvas c){
        float u=screenH;
        p.setColor(0x99071317);c.drawRoundRect(new RectF(18,16,screenW*.34f,u*.13f),14,14,p);
        drawText(c,"ЭХО  •  ОСКОЛКИ "+shards+"/3",34,u*.085f,u*.032f,0xffd6fff1);
        drawText(c,"ЦЕЛОСТНОСТЬ "+hp+"%",screenW*.72f,u*.085f,u*.03f,hp>30?0xffd7eee4:0xffff887c);
        float bx=screenW*.12f, by=u*.78f, rad=u*.105f;
        p.setColor(0x447bdbca);c.drawCircle(bx,by,rad,p);
        p.setColor(0x887bdbca);c.drawCircle(bx+joyX*rad*.65f,by-joyY*rad*.65f,rad*.42f,p);
        drawButton(c,screenW*.88f,u*.76f,"ЭХО",0xff6ed6c1);
        drawButton(c,screenW*.77f,u*.88f,"ИМПУЛЬС",0xffd9a66d);
        drawText(c,shards>=3?"ДОЙДИ ДО МАЯКА":"СОБЕРИ ОСКОЛКИ",screenW*.43f,u*.95f,u*.025f,0xffd7eee4);
        p.setColor(0x99dffff4);p.setStrokeWidth(2);
        c.drawLine(screenW*.5f-8,u*.49f,screenW*.5f+8,u*.49f,p);
        c.drawLine(screenW*.5f,u*.49f-8,screenW*.5f,u*.49f+8,p);
    }
    private void drawButton(Canvas c,float x,float y,String label,int col){
        float r=screenH*.07f;p.setColor(0x665a8e82);c.drawCircle(x,y,r*1.22f,p);
        p.setColor(col);c.drawCircle(x,y,r,p);
        p.setColor(0xff10221f);p.setTextSize(screenH*.022f);p.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        float tw=p.measureText(label);c.drawText(label,x-tw/2,y+screenH*.008f,p);
    }

    private void activateEcho(){
        for(Enemy e:enemies)if(dist(px,py,e.x,e.y)<5.0)e.stun=150;
        echoTicks=30;
    }
    private void activatePulse(){
        for(Enemy e:enemies)if(dist(px,py,e.x,e.y)<2.0)e.stun=90;
        pulseTicks=18;
    }

    @Override public boolean onTouchEvent(MotionEvent ev){
        float x=ev.getX(),y=ev.getY();
        int action=ev.getActionMasked(), index=ev.getActionIndex(), id=ev.getPointerId(index);
        if(!started){
            if(action==MotionEvent.ACTION_DOWN){started=true;lastFrame=SystemClock.uptimeMillis();invalidate();return true;}
            return true;
        }
        if(action==MotionEvent.ACTION_DOWN||action==MotionEvent.ACTION_POINTER_DOWN){
            if(x<screenW*.34f && leftPointer==-1){
                leftPointer=id;leftBaseX=screenW*.12f;leftBaseY=screenH*.78f;leftNowX=x;leftNowY=y;updateJoy();
            }else if(x>screenW*.68f && y>screenH*.58f){
                if(x>screenW*.82f && y<screenH*.86f)activateEcho();
                else if(x>screenW*.70f && y>screenH*.82f)activatePulse();
                else {lookPointer=id;lastLookX=x;}
            }else{lookPointer=id;lastLookX=x;}
            return true;
        }
        if(action==MotionEvent.ACTION_MOVE){
            for(int i=0;i<ev.getPointerCount();i++){
                int pid=ev.getPointerId(i);
                if(pid==leftPointer){leftNowX=ev.getX(i);leftNowY=ev.getY(i);updateJoy();}
                else if(pid==lookPointer){float nx=ev.getX(i);angle+=(nx-lastLookX)*0.0065;lastLookX=nx;}
            }
            return true;
        }
        if(action==MotionEvent.ACTION_UP||action==MotionEvent.ACTION_POINTER_UP||action==MotionEvent.ACTION_CANCEL){
            if(id==leftPointer){leftPointer=-1;joyX=joyY=0;}
            if(id==lookPointer)lookPointer=-1;
            return true;
        }
        return true;
    }
    private void updateJoy(){
        float r=screenH*.105f;
        joyX=Math.max(-1,Math.min(1,(leftNowX-leftBaseX)/r));
        joyY=Math.max(-1,Math.min(1,(leftBaseY-leftNowY)/r));
        float m=(float)Math.hypot(joyX,joyY);
        if(m>1){joyX/=m;joyY/=m;}
    }
}
