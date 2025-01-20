package opp.services;

import opp.dao.LocationRepository;
import opp.domain.Location;

import java.util.List;

public interface LocationService {
    List<Location> listAll();

    Location createLocation(Location location);
}
