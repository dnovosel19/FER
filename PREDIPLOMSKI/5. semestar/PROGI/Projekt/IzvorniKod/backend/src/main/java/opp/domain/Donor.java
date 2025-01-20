package opp.domain;

import jakarta.persistence.*;

import java.util.LinkedHashSet;
import java.util.Set;

@Entity
@Table(name = "donor")
public class Donor {
	@Id
	@GeneratedValue
	@Column(name = "iddonor", nullable = false)
	private Integer id;

	@Column(name = "username", nullable = false, length = Integer.MAX_VALUE)
	private String username;

	@Column(name = "password", nullable = false, length = Integer.MAX_VALUE)
	private String password;

	@Column(name = "ime", nullable = false, length = Integer.MAX_VALUE)
	private String name;

	@Column(name = "prezime", nullable = false, length = Integer.MAX_VALUE)
	private String surname;

	@Column(name = "oib", nullable = false)
	private String oib;

	@OneToMany(mappedBy = "donor")
	Set<DonorAppointment> donorAppointments = new LinkedHashSet<>();

	public Donor() {
	}

	public Donor(String username, String password, String name, String surname, String oib) {
		this.username = username;
		this.password = password;
		this.name = name;
		this.surname = surname;
		this.oib = oib;
	}

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getUsername() {
		return username;
	}

	public void setUsername(String username) {
		this.username = username;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getSurname() {
		return surname;
	}

	public void setSurname(String surname) {
		this.surname = surname;
	}

	public String getOib() {
		return oib;
	}

	public void setOib(String oib) {
		this.oib = oib;
	}

	@Override
	public String toString() {
		return "Donor{" +
				"id=" + id +
				", username='" + username + '\'' +
				", password='" + password + '\'' +
				", name='" + name + '\'' +
				", surname='" + surname + '\'' +
				", oib='" + oib + '\'' +
				'}';
	}
}