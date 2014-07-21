package mx.devf.alemolina.condesaaccesible;

import android.content.Context;
import android.os.AsyncTask;
import android.widget.Toast;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by alemolina on 7/18/14.
 */
public class HTTPTask extends AsyncTask<String, Integer, Double> {

    private Context applicationContext;

    @Override
    protected Double doInBackground(String... strings) {
        postData(strings[0], strings[1], strings[2]);
        return null;
    }

    protected void onPostExecute(Double result) {
        //  pb.setVisibility(View.GONE);
        Toast.makeText(getApplicationContext(), "UBICACION GUARDADA", Toast.LENGTH_LONG).show();
    }

    protected void onProgressUpdate(Integer... progress) {
        //pb.setProgress(progress[0]);
    }

    public void postData(String latitud, String longitud, String tipo) {
        // Create a new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost("http://pepo27devf.appspot.com/generarPunto");

        try {
            // Add your data
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();

            nameValuePairs.add(new BasicNameValuePair("latitud", latitud));
            nameValuePairs.add(new BasicNameValuePair("longitud", longitud));
            nameValuePairs.add(new BasicNameValuePair("tipo", tipo));

            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

            // Execute HTTP Post Request
            HttpResponse response = httpclient.execute(httppost);

        } catch (ClientProtocolException e) {
            // TODO Auto-generated catch block
        } catch (IOException e) {
            // TODO Auto-generated catch block
        }
    }

    public Context getApplicationContext() {
        return applicationContext;
    }

    public void setApplicationContext(Context applicationContext) {
        this.applicationContext = applicationContext;
    }
}