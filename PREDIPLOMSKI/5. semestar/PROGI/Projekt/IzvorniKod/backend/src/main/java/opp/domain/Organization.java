package opp.domain;

import jakarta.persistence.*;

import java.util.LinkedHashSet;
import java.util.Set;

@Entity
@Table(name = "ustanova")
public class Organization {
	@Id
	@GeneratedValue
	@Column(name = "idustanova", nullable = false)
	private Integer id;

	@Column(name = "adminusername", nullable = false, length = Integer.MAX_VALUE)
	private String adminUsername;

	@Column(name = "adminpassword", nullable = false, length = Integer.MAX_VALUE)
	private String adminPassword;

	@Column(name = "imeadmin", nullable = false, length = Integer.MAX_VALUE)
	private String adminName;

	@Column(name = "prezadmin", nullable = false, length = Integer.MAX_VALUE)
	private String adminSurname;

	@ManyToOne(fetch = FetchType.LAZY, optional = false)
	@JoinColumn(name = "idlokacije", nullable = false)
	private Location location;

	@ManyToOne(fetch = FetchType.LAZY, optional = false)
	@JoinColumn(name = "idvrste", nullable = false)
	private OrganizationType organizationType;

	@Column(name = "naziv", length = Integer.MAX_VALUE)
	private String naziv;

	@OneToMany(mappedBy = "organization")
	private Set<DonationAction> donationActions = new LinkedHashSet<>();

	@OneToMany(mappedBy = "organization")
	private Set<Donation> donations = new LinkedHashSet<>();

	@OneToMany(mappedBy = "organization")
	private Set<BloodSupply> bloodSupplies = new LinkedHashSet<>();

	public Organization() {
	}

	public Organization(String adminUsername, String adminPassword, String adminName, String adminSurname,String naziv, Location location, OrganizationType organizationType) {
		this.adminUsername = adminUsername;
		this.adminPassword = adminPassword;
		this.adminName = adminName;
		this.adminSurname = adminSurname;
		this.location = location;
		this.organizationType = organizationType;
		this.naziv = naziv;
	}

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getAdminUsername() {
		return adminUsername;
	}

	public void setAdminUsername(String adminUsername) {
		this.adminUsername = adminUsername;
	}

	public String getAdminPassword() {
		return adminPassword;
	}

	public void setAdminPassword(String adminPassword) {
		this.adminPassword = adminPassword;
	}

	public String getAdminName() {
		return adminName;
	}

	public void setAdminName(String adminName) {
		this.adminName = adminName;
	}

	public String getAdminSurname() {
		return adminSurname;
	}

	public void setAdminSurname(String adminSurname) {
		this.adminSurname = adminSurname;
	}

	public Location getLocation() {
		return location;
	}

	public void setLocation(Location location) {
		this.location = location;
	}

	public OrganizationType getOrganizationType() {
		return organizationType;
	}

	public void setOrganizationType(OrganizationType organizationType) {
		this.organizationType = organizationType;
	}

	public String getNaziv() {
		return naziv;
	}

	public void setNaziv(String naziv) {
		this.naziv = naziv;
	}

	public Set<DonationAction> getDonationActions() {
		return donationActions;
	}

	public void setDonationActions(Set<DonationAction> donationActions) {
		this.donationActions = donationActions;
	}

	public Set<Donation> getDonations() {
		return donations;
	}

	public void setDonations(Set<Donation> donations) {
		this.donations = donations;
	}

	public Set<BloodSupply> getBloodSupplies() {
		return bloodSupplies;
	}

	public void setBloodSupplies(Set<BloodSupply> bloodSupplies) {
		this.bloodSupplies = bloodSupplies;
	}

	@Override
	public String toString() {
		return "Organization{" +
				"id=" + id +
				", adminUsername='" + adminUsername + '\'' +
				", adminPassword='" + adminPassword + '\'' +
				", adminName='" + adminName + '\'' +
				", adminSurname='" + adminSurname + '\'' +
				", naziv='" + naziv + '\'' +
				'}';
	}
}