package opp.services.impl;

import opp.dao.LocationRepository;
import opp.domain.Location;
import opp.services.LocationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.util.Assert;

import java.util.List;

@Service
public class LocationServiceJpa implements LocationService {
	@Autowired
	private LocationRepository locationRepo;


	@Override
	public List<Location> listAll() {
		return locationRepo.findAll();
	}

	@Override
	public Location createLocation(Location location) {
		Assert.notNull(location, "Location object must be passed.");
		Assert.isNull(location.getId(), "Location must have an ID.");

//        String s = location.getCity();
        //
        return locationRepo.save(location);
    }
}
