package opp.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.dao.DaoAuthenticationProvider;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configurers.AbstractHttpConfigurer;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;

import static org.springframework.security.config.Customizer.withDefaults;

@Configuration
public class CustomSecurityConfig {

	@Autowired
	private PasswordEncoder passwordEncoder;

	@Bean
	public UserDetailsService customerUserDetailsService() {
		return new CustomUserDetailsService();
	}

	@Bean
	public DaoAuthenticationProvider authenticationProvider2() {
		DaoAuthenticationProvider authProvider = new DaoAuthenticationProvider();
		authProvider.setUserDetailsService(customerUserDetailsService());
		authProvider.setPasswordEncoder(passwordEncoder);
		authProvider.setHideUserNotFoundExceptions(false);

		return authProvider;
	}

	@Bean
	public SecurityFilterChain filterChainDonor(HttpSecurity http) throws Exception {
		http.authenticationProvider(authenticationProvider2());
		http.authorizeHttpRequests(authorize -> authorize.anyRequest().permitAll());

		http.formLogin(login -> login.loginProcessingUrl("/login")
				.successHandler((request, response, authentication) -> {
					if (authentication.getPrincipal() instanceof CustomUserDetails customUserDetails) {
						response.setHeader("id", String.valueOf(customUserDetails.getId()));
						response.setHeader("type", customUserDetails.getType());
					} else {
						response.setStatus(500);
					}
				})
				.failureHandler((request, response, exception) -> {
					if (exception.getClass().getSimpleName().equals("UsernameNotFoundException")) {
						response.setStatus(406);
					}

					response.setStatus(401);
				}));
		http.logout(logout -> logout.logoutUrl("/logout")
				.logoutSuccessHandler((request, response, authentication) -> response.setStatus(200))
				.invalidateHttpSession(true));
		http.httpBasic(withDefaults());
		http.csrf(AbstractHttpConfigurer::disable);
		return http.build();
	}
}