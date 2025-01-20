package opp.dao;

import opp.domain.OrganizationType;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.stereotype.Repository;

@Repository
@EnableJpaRepositories
public interface OrganizationTypeRepository extends JpaRepository<OrganizationType, Long> {

}
