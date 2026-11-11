# Decode the user's installed KTEX/BC3 thumbnails locally; no game art is bundled.
if (-not ('ShankCoop.Texture' -as [type])) {
Add-Type -ReferencedAssemblies System.Drawing -TypeDefinition @'
using System;
using System.IO;
using System.Drawing;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;
namespace ShankCoop {
 public static class Texture {
  static int U16(byte[] b,int p) { return b[p]|(b[p+1]<<8); }
  static int[] RGB(int c) { int r=(c>>11)&31,g=(c>>5)&63,v=c&31; return new int[]{(r<<3)|(r>>2),(g<<2)|(g>>4),(v<<3)|(v>>2)}; }
  public static Bitmap Load(string path) {
   byte[] b=File.ReadAllBytes(path);
   if(b.Length<18 || b[0]!=75 || b[1]!=84 || b[2]!=69 || b[3]!=88 || BitConverter.ToUInt32(b,4)!=0x02010000) throw new InvalidDataException("Unsupported KTEX thumbnail");
   int w=U16(b,8),h=U16(b,10),size=BitConverter.ToInt32(b,14);
   if(w<1 || h<1 || w>4096 || h>4096 || size!=((w+3)/4)*((h+3)/4)*16 || b.Length!=18+size) throw new InvalidDataException("Invalid KTEX dimensions");
   byte[] pixels=new byte[w*h*4]; int pos=18;
   for(int by=0;by<h;by+=4) for(int bx=0;bx<w;bx+=4) {
    int[] a=new int[8];a[0]=b[pos];a[1]=b[pos+1];
    if(a[0]>a[1]) { for(int j=2;j<8;j++) a[j]=((8-j)*a[0]+(j-1)*a[1])/7; }
    else { for(int j=2;j<6;j++) a[j]=((6-j)*a[0]+(j-1)*a[1])/5; a[6]=0;a[7]=255; }
    ulong ab=0;for(int j=0;j<6;j++) ab|=((ulong)b[pos+2+j])<<(8*j);
    int[][] c=new int[4][];c[0]=RGB(U16(b,pos+8));c[1]=RGB(U16(b,pos+10));c[2]=new int[3];c[3]=new int[3];
    for(int k=0;k<3;k++){c[2][k]=(2*c[0][k]+c[1][k])/3;c[3][k]=(c[0][k]+2*c[1][k])/3;}
    uint cb=BitConverter.ToUInt32(b,pos+12);
    for(int y=0;y<4;y++) for(int x=0;x<4;x++) {
     int n=y*4+x,ai=(int)((ab>>(3*n))&7),ci=(int)((cb>>(2*n))&3);
     if(bx+x>=w || by+y>=h) continue;
     int at=((by+y)*w+bx+x)*4;pixels[at]=(byte)c[ci][2];pixels[at+1]=(byte)c[ci][1];pixels[at+2]=(byte)c[ci][0];pixels[at+3]=(byte)a[ai];
    }
    pos+=16;
   }
   Bitmap image=new Bitmap(w,h,PixelFormat.Format32bppArgb);
   BitmapData data=image.LockBits(new Rectangle(0,0,w,h),ImageLockMode.WriteOnly,PixelFormat.Format32bppArgb);
   try { for(int y=0;y<h;y++) Marshal.Copy(pixels,y*w*4,IntPtr.Add(data.Scan0,y*data.Stride),w*4); }
   finally {image.UnlockBits(data);}
   return image;
  }
 }
}
'@
}
$script:portraitCache=@{}
function Get-CoopPortrait([string]$Root,[string]$Skin) {
    $texture=$Skin
    if($Skin -eq 'classic') {$texture='classicshank'}
    if($Skin -eq 'luchador') {$texture='lucha'}
    if($Skin -eq 'superheroine') {$texture='superhero'}
    $file=Join-Path $Root ('data-pc\textures\ui\skin\skin_'+$texture+'.tex')
    if(!(Test-Path -LiteralPath $file)) {return $null}
    if(!$script:portraitCache.ContainsKey($file)) {$script:portraitCache[$file]=[ShankCoop.Texture]::Load($file)}
    return $script:portraitCache[$file]
}
function Close-CoopPortraits {
    foreach($image in $script:portraitCache.Values) {$image.Dispose()}
    $script:portraitCache.Clear()
}
