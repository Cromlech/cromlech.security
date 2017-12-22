cromlech.security
=================

``cromlech.security`` provides base security components and utilities to
cook your own security policy.


Protagonist and Interaction
---------------------------

The base of a security policy is to know the `who`.
For this effect, `cromlech.security` proposes three components.

The `Principal` component represents an actor in the application.
A principal is defined by a few attributes : an id, a title and a
description. By default, a principal exists : `unauthenticated_principal`.
It will the one used in every security context until a new one is set.

The `Interaction` component represents a security context in which
one or several principals interact with the application. Interactions
can be nested, to allow a change of security context, for specific
operations (masquarading, admin tasks...).

The `Protagonist` is a conceptual wrapper around a principal, marking it as
belonging to an active interaction.


Permissions
-----------

Permissions are very basic named components.
By default, they are registered in a specific registry :
`cromlech.security.registry.security_registry`.
Out-of-the-box, permissions don't have any specific methods.
They are bricks with which you can secure components.


Securing components
-------------------

Securing a component can be done in many ways.
̀cromlech.security` defines a security decorator that does the following :

  >>> @secured_component('permission name')
  ... class Document(object):
  ...     pass

Once the class is grokked by the `cromlech.security` grokker, a new
method is added to the class

  >>> assert getattr(Document, '__check__', None)

This method is pluggable (see below) but by default, it does the following :

  - Query all the `ISecurityCheck` subscriptions components registered
    for our object;

  - Iterate through them and calling them giving them :
    the protected object, the permission, the current security interaction;

During this iteration, as soon as an error occured, the iteration stops and
the error is returned.

As said earlier, the `__check__` method is pluggable :

  >>> @secured_component('permission name', security_checker=my_func)
  ... class Document(object):
  ...     pass

The function passed as an argument only need to respect the following
prototype :

  >>> def my_func(permission):
  ...     return None   # No error happened.

The return value of the security checker is either Non if the access
is granted or the value of the first error encountered, to deny the access.

Please note two things :

  - The `permission` attribute given to the `secured_component`
    decorator and gotten as a value in security checker function
    is NOT of a specific type. It can be a string, a Permission
    object or anything else.

  - The error value returned must be derived from BaseException
    as it will be raised later in the process.

This very loose implementation is a design choice, to allow
very flexible security architecture.

To finish, the __check__ method is not called magically.
In order to apply this security framework, there is one last layer,
usually involving the view or model lookup of your application, depending
on the component you are securing.

Let's assume you have a lookup model for your Document, based on an id:

  >>> doc = my_lookup_method('document-42')

We can wrap it with our security decorator:

  >>> from cromlech.security import component_protector
  >>> doc = component_protector(my_lookup_method)('document-42')

If the __check__ method of your document is successful, you get the document
object. If an security error occurs, the error is raised.
