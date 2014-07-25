package mx.devf.alemolina.condesaaccesible;

import com.google.android.gms.maps.model.LatLng;

/**
 * Created by rickmartz on 24/07/14.
 */
public class PlaceDot {

    private LatLng place;
    private int score;

    public LatLng getPlace() {
        return place;
    }

    public void setPlace(LatLng place) {
        this.place = place;
    }

    public int getScore() {
        return score;
    }

    public void setScore(int score) {
        this.score = score;
    }

}
