package opp.controller;

import opp.domain.Donor;
import opp.domain.Organization;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import java.util.Collection;
import java.util.List;
import java.util.Optional;

public class CustomUserDetails implements UserDetails {

	private final Optional<Donor> donor;
	private final Optional<Organization> organization;

	public CustomUserDetails(Donor donor) {
		this.donor = Optional.ofNullable(donor);
		this.organization = Optional.empty();
	}

	public CustomUserDetails(Organization organization) {
		this.donor = Optional.empty();
		this.organization = Optional.ofNullable(organization);
	}

	@Override
	public Collection<? extends GrantedAuthority> getAuthorities() {
		if (donor.isPresent()) {
			return List.of(new SimpleGrantedAuthority("ROLE_USER"));
		} else if (organization.isPresent()) {
			return List.of(new SimpleGrantedAuthority("ROLE_ADMIN"));
		} else {
			return List.of();
		}
	}

	@Override
	public String getPassword() {
		if (donor.isPresent()) {
			return donor.get().getPassword();
		} else if (organization.isPresent()) {
			return organization.get().getAdminPassword();
		} else {
			return null;
		}
	}

	@Override
	public String getUsername() {
		if (donor.isPresent()) {
			return donor.get().getUsername();
		} else if (organization.isPresent()) {
			return organization.get().getAdminUsername();
		} else {
			return null;
		}
	}

	@Override
	public boolean isAccountNonExpired() {
		return true;
	}

	@Override
	public boolean isAccountNonLocked() {
		return true;
	}

	@Override
	public boolean isCredentialsNonExpired() {
		return true;
	}

	@Override
	public boolean isEnabled() {
		return true;
	}

	public Optional<Donor> getDonor() {
		return donor;
	}

	public Optional<Organization> getOrganization() {
		return organization;
	}

	public String getType() {
		if (donor.isPresent()) {
			return "donor";
		} else if (organization.isPresent()) {
			return "organization";
		} else {
			return null;
		}
	}

	public Integer getId() {
		if (donor.isPresent()) {
			return donor.get().getId();
		} else if (organization.isPresent()) {
			return organization.get().getId();
		} else {
			return null;
		}
	}
}
