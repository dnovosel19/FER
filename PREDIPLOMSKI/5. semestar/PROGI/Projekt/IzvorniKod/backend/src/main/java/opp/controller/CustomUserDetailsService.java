package opp.controller;

import opp.domain.Donor;
import opp.domain.Organization;
import opp.services.BloodDonorService;
import opp.services.OrganizationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class CustomUserDetailsService implements UserDetailsService {

	@Autowired
	private BloodDonorService donorService;

	@Autowired
	private OrganizationService organizationService;

	@Override
	public UserDetails loadUserByUsername(String username) {
		Optional<Donor> donor = donorService.findByUsername(username);
		if (donor.isPresent()) return new CustomUserDetails(donor.get());

		Optional<Organization> organization = organizationService.findByUsername(username);
		if (organization.isPresent()) return new CustomUserDetails(organization.get());

		throw new UsernameNotFoundException("No user '" + username + "' found");
	}
}
