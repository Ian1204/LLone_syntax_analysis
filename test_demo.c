int main(){
    int a = 0;
    int b = a + 1;
    int c = b*2;
    if(a||b){
        if(a&&b){
            if(!a){
                a+=b;
                b-=c;
                c*=a;
                a/=a;
                b%=b;
                b++;
            }
        }
    }
    return 0;
}