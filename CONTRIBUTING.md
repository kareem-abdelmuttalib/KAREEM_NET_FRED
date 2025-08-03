# Contribution Guidelines

## Security Protocols

1. All credential handling must use getpass or equivalent
2. Network operations require Tor SOCKS5 proxy fallback
3. MAC address functions must include validation regex:
   ^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$

## Code Standards

- Network functions:
  - Minimum 3-second delay after Tor NEWNYM
  - Dual verification for IP/geolocation
  - Timeout handling for all requests

- Error Handling:
  - Fail-closed for security operations
  - Graceful degradation for non-critical features
  - Root privilege verification

## Testing Requirements

New features must include:
1. Tor circuit validation tests
2. MAC address format verification
3. Geolocation API mock tests