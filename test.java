package com.justsy.url;
 import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.entity.UrlEncodedFormEntity; 
import org.apache.http.client.methods.HttpPost; 
import org.apache.http.impl.client.DefaultHttpClient; 
import org.apache.http.message.BasicNameValuePair; 
import org.apache.http.protocol.HTTP; 
import org.apache.http.util.EntityUtils; 
import android.app.Activity; 
import android.os.Bundle; 
public class HttpURLActivity extends Activity {
     @Override 
       public void onCreate(Bundle savedInstanceState) { 
        super.onCreate(savedInstanceState);
        System.out.println("start url..."); 
        String url = "http://192.168.2.112:8080/JustsyApp/Applet"; 
        // 第一步，创建HttpPost对象 
        HttpPost httpPost = new HttpPost(url); 
        // 设置HTTP POST请求参数必须用NameValuePair对象 
        List<NameValuePair> params = new ArrayList<NameValuePair>(); 
        params.add(new BasicNameValuePair("action", "downloadAndroidApp")); 
        params.add(new BasicNameValuePair("packageId", "89dcb664-50a7-4bf2-aeed-49c08af6a58a")); 
        params.add(new BasicNameValuePair("uuid", "test_ok1")); 
        HttpResponse httpResponse = null; 
        try { // 设置httpPost请求参数 
        httpPost.setEntity(new UrlEncodedFormEntity(params, HTTP.UTF_8)); 
        httpResponse = new DefaultHttpClient().execute(httpPost);
         //System.out.println(httpResponse.getStatusLine().getStatusCode()); 
         if (httpResponse.getStatusLine().getStatusCode() == 200) {
             // 第三步，使用getEntity方法活得返回结果 
             String result = EntityUtils.toString(httpResponse.getEntity());
              System.out.println("result:" + result); T.displayToast(HttpURLActivity.this, "result:" + result);
               } } catch (ClientProtocolException e) {
                 e.printStackTrace(); } catch (IOException e) { 
                    e.printStackTrace(); 
                    } 
                    System.out.println("end url..."); 
                    setContentView(R.layout.main);
                     } }