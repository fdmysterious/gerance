Feature: Test

    This features tests the parsing magic of gerance

    Rule: My error managment

        My error must be managed for good

        @covers.MyRequirementID0001
        @another_tag
        @covers.MyRequirementID0002[]
        @covers.MyRequirementID0003[v2.4.5]
        Scenario: My error is set
            Given stuff
            When another stuff
            Then consequences

        @covers.MyRequirementID0004
        Scenario: My error is clear
            Given new stuff
            When yet another stuff
            Then consequences are canceled

    @covers.MyRequirementID30429[A]
    Scenario: Root scenario
        Given yeah
        When booh
        Then not happy