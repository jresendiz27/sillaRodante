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
import org.apache.http.impl.client.BasicResponseHandler;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.message.BasicNameValuePair;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Created by alemolina on 7/18/14.
 */
public class HTTPTask extends AsyncTask<String, Integer, String> {

    private Context applicationContext;

    @Override
    protected String doInBackground(String... strings) {
        if (strings[0].equals("sendScore")) {
            return postData(strings);
        } else if (strings[0].equals("getPoints")) {
            return getPoints(strings);
        } else {
            return null;
        }
    }

    protected void onPostExecute(Double result) {
        //  pb.setVisibility(View.GONE);
        Toast.makeText(getApplicationContext(), "UBICACION GUARDADA", Toast.LENGTH_LONG).show();
    }

    protected void onProgressUpdate(Integer... progress) {
        //pb.setProgress(progress[0]);
    }

    public String getPoints(String[] parametros) {
        // Create a new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost(parametros[1]);
        String respuesta = "";
        try {
            // Add your data
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();

            nameValuePairs.add(new BasicNameValuePair("latitudOrigen", parametros[2]));
            nameValuePairs.add(new BasicNameValuePair("longitudOrigen", parametros[3]));

            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

            // Execute HTTP Post Request
            HttpResponse response = httpclient.execute(httppost);
            respuesta  = new BasicResponseHandler().handleResponse(response);
            return respuesta;

        } catch (ClientProtocolException e) {
            // TODO Auto-generated catch block
            return  respuesta;
        } catch (IOException e) {
            // TODO Auto-generated catch block
            return respuesta;
        }
    }

    public String postData(String[] parametros) {
        // Create a new HttpClient and Post Header
        HttpClient httpclient = new DefaultHttpClient();
        HttpPost httppost = new HttpPost(parametros[1]);

        try {
            // Add your data
            List<NameValuePair> nameValuePairs = new ArrayList<NameValuePair>();

            nameValuePairs.add(new BasicNameValuePair("latitud", parametros[2]));
            nameValuePairs.add(new BasicNameValuePair("longitud", parametros[3]));
            nameValuePairs.add(new BasicNameValuePair("tipo", parametros[4]));

            httppost.setEntity(new UrlEncodedFormEntity(nameValuePairs));

            // Execute HTTP Post Request
            HttpResponse response = httpclient.execute(httppost);

        } catch (ClientProtocolException e) {
            // TODO Auto-generated catch block
        } catch (IOException e) {
            // TODO Auto-generated catch block
        }
        return null;
    }

    public Context getApplicationContext() {
        return applicationContext;
    }

    public void setApplicationContext(Context applicationContext) {
        this.applicationContext = applicationContext;
    }
}