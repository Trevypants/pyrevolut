from datetime import datetime
import pendulum

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID

from pyrevolut.utils.datetime import DateTime, to_datetime


def gen_public_private_cert(
    expiration_dt: datetime | DateTime | str | int | float,
    country: str,
    email_address: str | None = None,
    common_name: str | None = None,
    state: str | None = None,
    locality: str | None = None,
    organization: str | None = None,
    organization_unit: str | None = None,
    save_location_public: str | None = "publiccert.cer",
    save_location_private: str | None = "privatecert.pem",
):
    """
    Method to generate a X509 RSA key pair and save it to a file.
    The key pair is used to create a client-assertion JWT for Revolut.

    Parameters
    ----------
    expiration_dt : datetime | DateTime | str | int | float
        The expiration datetime (UTC) of the certificate.
        This can be a datetime object, a DateTime object, a string, an integer, or a float.
    country : str
        The country of the certificate (2-letter code)
    email_address : str | None, optional
        The email address of the certificate.
    common_name : str | None, optional
        The common name (eg, fully qualified host name) of the certificate.
    state : str | None, optional
        The state (full name) of the certificate.
    locality : str | None, optional
        The locality (eg, city) of the certificate.
    organization : str | None, optional
        The organization (eg, company) of the certificate.
    organization_unit : str | None, optional
        The organization unit (eg, section) of the certificate.
    save_location_public : str | None, optional
        The location to save the public key.
        If None, the public key will not be saved.
        Default is "publiccert.cer".
    save_location_private : str | None, optional
        The location to save the private key.
        If None, the private key will not be saved.
        Default is "privatecert.pem".

    Returns
    -------
    dict
        A dictionary containing the public and private keys (in bytes)
    """
    # Generate an RSA key pair
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

    # Create a certificate
    names = [x509.NameAttribute(NameOID.COUNTRY_NAME, country)]
    if email_address is not None:
        names.append(x509.NameAttribute(NameOID.EMAIL_ADDRESS, email_address))
    if common_name is not None:
        names.append(x509.NameAttribute(NameOID.COMMON_NAME, common_name))
    if state is not None:
        names.append(x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state))
    if locality is not None:
        names.append(x509.NameAttribute(NameOID.LOCALITY_NAME, locality))
    if organization is not None:
        names.append(x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization))
    if organization_unit is not None:
        names.append(
            x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, organization_unit)
        )
    subject = issuer = x509.Name(names)

    # Create a self-signed certificate
    cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(pendulum.now(tz="UTC"))
        .not_valid_after(to_datetime(dt=expiration_dt))
        .sign(private_key, hashes.SHA256())
    )

    # Get the public/private key in bytes
    public_key = cert.public_bytes(serialization.Encoding.PEM)
    private_key = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Save the private key to a file if save_location is provided
    if save_location_private is not None:
        with open(save_location_private, "wb") as f:
            f.write(private_key)

    # Save the public key to a file if save_location is provided
    if save_location_public is not None:
        with open(save_location_public, "wb") as f:
            f.write(public_key)

    # Return the keys
    return {
        "public": public_key,
        "private": private_key,
    }
