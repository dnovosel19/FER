package opp.dao;

import opp.domain.BloodSupply;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
@EnableJpaRepositories
public interface BloodSuppliesRepository extends JpaRepository<BloodSupply, Long> {

    List<BloodSupply> findByOrganizationId(Long organizationId);
}
