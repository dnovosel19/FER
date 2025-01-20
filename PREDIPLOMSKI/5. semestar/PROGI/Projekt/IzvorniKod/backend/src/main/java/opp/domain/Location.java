package opp.domain;

import jakarta.persistence.*;

import java.util.LinkedHashSet;
import java.util.Set;

@Entity
@Table(name = "lokacija")
public class Location {
	@Id
	@Column(name = "idlokacija", nullable = false)
	private Integer id;

	@Column(name = "naziv", nullable = false, length = Integer.MAX_VALUE)
	private String name;

	@Column(name = "koordinate", nullable = false, length = Integer.MAX_VALUE)
	private String coordinates;

	@OneToMany(mappedBy = "location")
	private Set<DonationAction> donationActions = new LinkedHashSet<>();

	@OneToMany(mappedBy = "location")
	private Set<Donation> donations = new LinkedHashSet<>();

	@OneToMany(mappedBy = "location")
	private Set<Organization> organizations = new LinkedHashSet<>();

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getCoordinates() {
		return coordinates;
	}

	public void setCoordinates(String coordinates) {
		this.coordinates = coordinates;
	}

	public Set<DonationAction> getAkcijadarivanjas() {
		return donationActions;
	}

	public void setAkcijadarivanjas(Set<DonationAction> donationActions) {
		this.donationActions = donationActions;
	}

	public Set<Donation> getDonacijas() {
		return donations;
	}

	public void setDonacijas(Set<Donation> donations) {
		this.donations = donations;
	}

	public Set<Organization> getOrganizations() {
		return organizations;
	}

	public void setOrganizations(Set<Organization> organizations) {
		this.organizations = organizations;
	}

	@Override
	public String toString() {
		return "Location{" +
				"id=" + id +
				", name='" + name + '\'' +
				", coordinates='" + coordinates + '\'' +
				", donationActions=" + donationActions +
				", donations=" + donations +
				", organizations=" + organizations +
				'}';
	}
}