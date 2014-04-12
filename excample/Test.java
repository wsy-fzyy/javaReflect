public class Test {
    public Test() {System.out.println("default construction");}
    
    public Test(String str) {System.out.println("construction " + str);}

    public void show(int n, String str) {System.out.println("show " + n + " " + str);}

    public static void main(String[] args) {
        String cls = "Test";

        #cls obj1 = new #cls();
        #cls obj2 = new #cls("okey");
        obj1.show(10, "hello");
    }
}
