import java.io.BufferedReader; 
import java.io.InputStreamReader; 
import java.net.HttpURLConnection; 
import java.net.URL;

public class getjava {
     public static void main(String[] args) {
         try {
         // Create URL 
         URL url = new URL("http://192.168.1.4/search/?code=600352&days=10&date=20230125"); // Create connection 
         HttpURLConnection con = (HttpURLConnection) 
         url.openConnection(); 
         // Set request method 
         con.setRequestMethod("GET"); 
         // Get response 
         BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream())); 
         String inputLine; 
         StringBuffer response = new StringBuffer(); 
         
         while ((inputLine = in.readLine()) != null) {
             response.append(inputLine);
             } in.close(); 
             // Print response 
            String tt=new String(response.toString().getBytes("gb2312"),"gbk");
             System.out.println(tt); 
            } catch (Exception ex) { 
                ex.printStackTrace(); 
            } 
        } 
    }