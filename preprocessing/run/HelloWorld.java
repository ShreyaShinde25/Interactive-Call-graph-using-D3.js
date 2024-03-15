public class HelloWorld {
    public static void main(String[] args) {
        int i = 10;
        System.out.println("Hello World");
        recMethod(100);
    }

    public static int singleLine(int n) {
        int a = n + 3;
        return a + rec(100);
    }

    public static int multiLine(int n) {
        int a1 = n + 1;
        int a2 = n + 1;
        int a3 = n + 1;
        int a4 = n + 1;
        int a5 = n + 1;
        int a6 = n + 1;
        int a7 = n + 1;
        int a8 = n + 1;
        int a9 = n + 1;
        int a10 = n + 1;
        return a1 + a2 + a3 + a4 + a5 + a6 + a7 + a8 + a9 + a10 + rec(100);
    }

    public static int multiInput(int n1, int n2, int n3, int n4, int n5) {
        return n1 + n2 + n3 + n4 + n5 + rec(100);
    }

    public static int rec(int n) {
        if (n == 1) {
            return 1;
        }
        return 1 + rec(n-1);
    }

    public static int recMethod(int n) {
        if (n == 1){
            return 1; 
        }
        return singleLine(n) +
        multiLine(n) +
        multiInput(n,n,n,n,n)+
        recMethod(n-1);
    }
}