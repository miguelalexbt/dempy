import dempy

def main():

    dempy.config.use_default()

    





    # adicionar objecto devices / sensors
    # devices de um certa annotation

    """ Datasets """

    ## Get all datasets

    all_datasets = dempy.datasets.get()

    ## Get tagged datasets
    
    red_datasets = dempy.datasets.get(tags=["red"])

    ## Count datasets

    datasets_count = dempy.datasets.count()

    ## Create dataset

    dataset = dempy.datasets.create(name = "Teste")  #suportar ambos
    
    ## Get dataset

    dempy.datasets.get(dataset.id)

    ## Get dataset's acquisitions

    acquisitions = dempy.datasets.get(dataset.id).acquisitions.get()

    ## Export dataset

    dempy.datasets.get(dataset.id).export(f"~/Desktop/{dataset.id}.zip")

    ## Delete dataset

    dempy.datasets.get(dataset.id).delete()

    """ Acquisitions """

    all_datasets = dempy.datasets.get()

    """ Organizations """

    ## Get all Organizations

    all_organizations = dempy.organizations.get()

    ## Count Organizations

    organizations_count = dempy.organizations.count()

    ## Create organization

    organization_VIDAL = dempy.organizations.create(dempy.Organization(name = "VIDAL"))
    organization_FEUP = dempy.organizations.create(dempy.Organization(name = "FEUP"))

    ## Get organization

    organization = dempy.organizations.get(organization_FEUP.id)

    ## Delete organization

    dempy.organizations.get(organization_VIDAL.id).delete()

    ## Add User to Organization
    
    user = dempy.users.create(dempy.User(firstName = "Nome 1", lastName = "Nome 2"))
    dempy.organizations.get(organization_FEUP.id).users.add(user.id)

    ## Get Users of Organization

    usersIDs = dempy.organizations.get(organization_FEUP.id).users.get()

    ## Get Number of Users of Organization

    count = dempy.organizations.get(organization_FEUP.id).users.count()

    ## Remove User from Organization

    dempy.organizations.get(organization_FEUP.id).users.remove(usersIDs[0])
    count = dempy.organizations.get(organization_FEUP.id).users.count()
    
    """ Users """
    
    ## Get all users

    all_users = dempy.users.get()

    ## Count users

    users_count = dempy.users.count()

    ## Create user

    user = dempy.users.create(dempy.User(firstName = "Nome 1", lastName = "Nome 2"))

    ## Get user

    dempy.users.get(user.id)

    ## Delete user

    dempy.users.get(user.id).delete()
  
if __name__	== "__main__":
	main()
