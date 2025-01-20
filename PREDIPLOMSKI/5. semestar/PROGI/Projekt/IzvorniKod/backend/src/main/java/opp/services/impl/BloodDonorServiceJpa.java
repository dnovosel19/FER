package opp.services.impl;

import jakarta.transaction.Transactional;
import opp.DTO.BloodDonorDTO;
import opp.DTO.LoginDTO;
import opp.dao.AppointmentRepository;
import opp.dao.BloodDonorRepository;
import opp.dao.DonationsRepository;
import opp.dao.OrganizationRepository;
import opp.domain.Donation;
import opp.domain.Donor;
import opp.domain.Organization;
import opp.services.BloodDonorService;
import opp.services.EntityMissingException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class BloodDonorServiceJpa implements BloodDonorService {

	@Autowired
	private OrganizationRepository organizationRepository;

    @Autowired
    private BloodDonorRepository bloodDonorRepository;

    @Autowired
    private AppointmentRepository appointmentRepository;

    @Autowired
    private DonationsRepository donationRepository;

	@Autowired
	PasswordEncoder encoder;

    public BloodDonorServiceJpa(BloodDonorRepository bloodDonorRepository) {
        this.bloodDonorRepository = bloodDonorRepository;
    }

    public ResponseEntity<?> addBloodDonor(@RequestBody BloodDonorDTO bloodDonorDTO) {
        try {
            System.out.println("Received registration request: " + bloodDonorDTO.toString());

            Donor existingUsernameUser = bloodDonorRepository.findByUsername(bloodDonorDTO.getUsername());
			Organization existingNameOrganization = organizationRepository.findByAdminUsername(bloodDonorDTO.getName());

            if (existingUsernameUser != null || existingNameOrganization != null) {
                System.out.println("Registration failed - Username already exists: " + bloodDonorDTO.getUsername());
                return ResponseEntity.status(HttpStatus.BAD_REQUEST).body("Username already exists");
            }


            System.out.println("Creating new donor with username: " + bloodDonorDTO.getUsername());

            Donor bloodDonor = new Donor(
            );
            bloodDonor.setUsername(bloodDonorDTO.getUsername());
			String encoded = encoder.encode(bloodDonorDTO.getPassword());
            bloodDonor.setPassword(encoded);
            bloodDonor.setName(bloodDonorDTO.getName());
            bloodDonor.setSurname(bloodDonorDTO.getSurname());
            bloodDonor.setOib(bloodDonorDTO.getOib());
            System.out.println(bloodDonor.toString());
            bloodDonorRepository.save(bloodDonor);

            String successMessage = "Registration successful for user " + bloodDonorDTO.getUsername() + " with ID: " + bloodDonor.getId();
            System.out.println(successMessage);

            return ResponseEntity.ok(Map.of("userType", "donor", "id", bloodDonor.getId()));
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("Error during registration");
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error during registration");
        }
    }

    @Transactional
    public void deleteDonorAndDonations(Long donorId) {
        donationRepository.deleteByDonorId(donorId);

        bloodDonorRepository.deleteById(donorId);
    }

	@Override
	public Optional<Donor> findByUsername(String username) {
		return Optional.ofNullable(bloodDonorRepository.findByUsername(username));
	}

	@Override
	public Donor fetch(long donorId) {
		return findById(donorId).orElseThrow(
				() -> new EntityMissingException(Donor.class, donorId)
		);
	}

	@Override
	public Optional<Donor> findById(long groupId) {
		return bloodDonorRepository.findById(groupId);
	}

}