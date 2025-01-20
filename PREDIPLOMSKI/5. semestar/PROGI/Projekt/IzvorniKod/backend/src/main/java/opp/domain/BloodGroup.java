package opp.domain;

import jakarta.persistence.*;

import java.util.LinkedHashSet;
import java.util.Set;

@Entity
@Table(name = "krvnagrupa")
public class BloodGroup {
	@Id
	@GeneratedValue
	@Column(name = "idgrupa", nullable = false)
	private Integer id;

	@Column(name = "tipgrupe", nullable = false, length = Integer.MAX_VALUE)
	private String bloodType;

	@OneToMany(mappedBy = "bloodGroup")
	private Set<Donation> donations = new LinkedHashSet<>();

	@OneToMany(mappedBy = "bloodGroup")
	private Set<BloodSupply> bloodSupplies = new LinkedHashSet<>();

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getBloodType() {
		return bloodType;
	}

	public void setBloodType(String bloodType) {
		this.bloodType = bloodType;
	}

	public Set<Donation> getDonacijas() {
		return donations;
	}

	public void setDonacijas(Set<Donation> donations) {
		this.donations = donations;
	}

	public Set<BloodSupply> getZalihakrvis() {
		return bloodSupplies;
	}

	public void setZalihakrvis(Set<BloodSupply> bloodSupplies) {
		this.bloodSupplies = bloodSupplies;
	}

	@Override
	public String toString() {
		return "BloodGroup{" +
				"id=" + id +
				", bloodType='" + bloodType + '\'' +
				", donations=" + donations +
				", bloodSupplies=" + bloodSupplies +
				'}';
	}
}