"""
Runs Default tests
Available Modules: http://testinfra.readthedocs.io/en/latest/modules.html

"""
import os
import testinfra.utils.ansible_runner

TESTINFRA_HOSTS = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_configuration_file(host):
    """
    Tests that the configuration file exists
    """
    os_family = host.ansible("setup")["ansible_facts"]["ansible_os_family"]
    if os_family == "RedHat":
        conf_file = "/etc/yum/yum-cron.conf"
    elif os_family == "Debian":
        conf_file = "/etc/apt/apt.conf.d/50unattended-upgrades"

    file = host.file(conf_file)

    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'
    assert file.contains('somerandomtestapp*')


def test_package_is_installed_running_and_enabled(host):
    """
    Tests that yum-cron or unnattended-upgrades is installed
    """
    os_family = host.ansible("setup")["ansible_facts"]["ansible_os_family"]
    if os_family == "RedHat":
        package = "yum-cron"
    elif os_family == "Debian":
        package = "unattended-upgrades"

    host_package = host.package(package)
    host_service = host.service(package)
    assert host_package.is_installed
    assert host_service.is_running
    assert host_service.is_enabled
