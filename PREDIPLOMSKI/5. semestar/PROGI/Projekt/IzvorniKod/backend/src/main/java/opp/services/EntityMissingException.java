package opp.services;

import org.springframework.web.bind.annotation.ResponseStatus;

import java.io.Serial;

import static org.springframework.http.HttpStatus.NOT_FOUND;

@ResponseStatus(NOT_FOUND)
public class EntityMissingException extends RuntimeException {

	@Serial
	private static final long serialVersionUID = 10L;

	public EntityMissingException(Class<?> cls, Object ref) {
		super("Entity with reference " + ref + " of " + cls + " not found.");
	}
}
