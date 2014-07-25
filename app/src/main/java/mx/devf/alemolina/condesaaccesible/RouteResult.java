package mx.devf.alemolina.condesaaccesible;

import com.google.android.gms.maps.model.LatLng;

import java.util.ArrayList;

/**
 * Created by rickmartz on 24/07/14.
 */
public class RouteResult {

    ArrayList<LatLng> route;
    ArrayList<PlaceDot> dots;


    public ArrayList<LatLng> getRoute() {
        return route;
    }

    public void setRoute(ArrayList<LatLng> route) {
        this.route = route;
    }

    public ArrayList<PlaceDot> getDots() {
        return dots;
    }

    public void setDots(ArrayList<PlaceDot> dots) {
        this.dots = dots;
    }
}
