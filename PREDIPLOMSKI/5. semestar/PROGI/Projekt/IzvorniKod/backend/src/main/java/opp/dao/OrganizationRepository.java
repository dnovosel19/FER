package opp.dao;

import opp.domain.Organization;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.stereotype.Repository;
import java.util.Optional;
@Repository
@EnableJpaRepositories
public interface OrganizationRepository extends JpaRepository<Organization, Long> {
    Organization findByAdminUsername(String username);
    Optional<Organization> findOneByAdminUsernameAndAdminPassword(String username, String password);
}
