package opp.domain;

import jakarta.persistence.*;

import java.util.LinkedHashSet;
import java.util.Set;

@Entity
@Table(name = "vrstaustanove")
public class OrganizationType {
	@Id
	@Column(name = "idvrste", nullable = false)
	private Integer id;

	@Column(name = "nazivvrste", nullable = false, length = Integer.MAX_VALUE)
	private String typeName;

	@OneToMany(mappedBy = "organizationType")
	private Set<Organization> ustanova = new LinkedHashSet<>();

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public String getTypeName() {
		return typeName;
	}

	public void setTypeName(String typeName) {
		this.typeName = typeName;
	}

	public Set<Organization> getUstanova() {
		return ustanova;
	}

	public void setUstanova(Set<Organization> ustanova) {
		this.ustanova = ustanova;
	}

}