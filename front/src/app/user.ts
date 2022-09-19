export class Contact {
    email: string | undefined;
    linkedin: string | undefined;
    github: string | undefined;
}

export class User {
    first_name: string | undefined;
    last_name: string | undefined;
    contact: Contact | undefined;
}
